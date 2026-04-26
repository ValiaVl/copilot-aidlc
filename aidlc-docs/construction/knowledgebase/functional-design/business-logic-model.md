# Business Logic Model — Team Knowledge Base

## Workflow 1: Sign In

```
1. User submits name via form
2. Trim and lowercase the name
3. Validate: name is non-empty → else show error
4. Query User table for matching name
5. IF found → use existing user
   ELSE → create new User record
6. Store user_id in session cookie
7. Redirect to home page (/)
```

## Workflow 2: Sign Out

```
1. Clear session cookie
2. Redirect to /signin
```

## Workflow 3: Create Article

```
1. Require authenticated session → else redirect to /signin
2. User fills in title, body, and tags (dynamic tag fields)
3. Validate title (non-empty, ≤200 chars)
4. Validate body (non-empty, ≤50,000 chars)
5. IF validation fails → re-render form with errors
6. Resolve tags:
   a. For each tag name: trim, lowercase, skip if empty
   b. Find existing Tag by name or create new Tag
7. Create Article record (title, body, author_id=session user, is_stale=False)
8. Create ArticleTag links for each resolved tag
9. Redirect to article detail page
```

## Workflow 4: Edit Article

```
1. Require authenticated session
2. Load article by ID → 404 if not found
3. Pre-fill form with current title, body, tags
4. User modifies fields
5. Validate title and body (same rules as creation)
6. IF validation fails → re-render form with errors
7. Update Article fields (title, body, updated_at=now)
8. Sync tags:
   a. Resolve new tag list (trim, lowercase, find-or-create)
   b. Remove ArticleTag links for tags no longer present
   c. Add ArticleTag links for newly added tags
9. Create EditLog entry (article_id, editor_id=session user, edited_at=now)
10. Redirect to article detail page
```

## Workflow 5: Toggle Stale Flag

```
1. Require authenticated session
2. Load article by ID → 404 if not found
3. Flip is_stale (True → False, False → True)
4. Save article
5. Return HTMX partial: updated stale banner + toggle button
```

## Workflow 6: Live Search

```
1. Receive search parameters: q (text query), tag (tag filter)
2. Build query:
   a. IF q is non-empty → filter Article WHERE title LIKE %q% OR body LIKE %q% (case-insensitive)
   b. IF tag is non-empty → join ArticleTag + Tag, filter WHERE tag.name = tag
   c. IF both → combine with AND
   d. IF neither → return all articles
3. Order by updated_at DESC
4. Return HTMX partial: filtered article list
```

## Workflow 7: Tag Filtering (via click)

```
1. User clicks a tag on an article card or detail page
2. Navigate to home with tag filter: /?tag=tagname
3. OR trigger HTMX request: GET /search?tag=tagname
4. Return filtered article list
```

## Workflow 8: Markdown Preview

```
1. User clicks "Preview" toggle on article form
2. HTMX sends current body content to POST /articles/preview
3. Server renders markdown to HTML
4. Sanitise HTML output (strip dangerous tags)
5. Return HTMX partial: rendered HTML
6. User clicks "Edit" toggle → show raw markdown textarea again
```

## Workflow 9: Add/Remove Tag Field (Dynamic)

```
1. User clicks "Add tag" button on article form
2. HTMX appends a new empty tag input field to the form
3. User can type tag name in the new field
4. User can remove a tag field by clicking its remove button
5. On form submit, all non-empty tag fields are collected
```

## Authentication Middleware

```
For every request (except /signin, /signout, static files):
1. Check session for user_id
2. IF user_id exists → load User, attach to request state
3. IF user_id missing → redirect to /signin
```
