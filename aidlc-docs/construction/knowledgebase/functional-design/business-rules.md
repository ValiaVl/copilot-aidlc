# Business Rules — Team Knowledge Base

## BR-1: User Identity

| Rule | Description |
|------|-------------|
| BR-1.1 | User name is required and must be non-empty after trimming whitespace |
| BR-1.2 | User name is stored lowercase for case-insensitive matching |
| BR-1.3 | If a user with the same name (case-insensitive) exists, reuse that record |
| BR-1.4 | If no matching user exists, create a new User record |
| BR-1.5 | Session stores `user_id`; all authenticated actions require a valid session |
| BR-1.6 | Unauthenticated requests redirect to `/signin`, then to `/` after sign-in |

## BR-2: Article Creation

| Rule | Description |
|------|-------------|
| BR-2.1 | Title is required, max 200 characters |
| BR-2.2 | Body is required, max 50,000 characters |
| BR-2.3 | Tags are optional (zero or more) |
| BR-2.4 | Author is set to the currently signed-in user (cannot be overridden) |
| BR-2.5 | `created_at` and `updated_at` are set to current timestamp on creation |
| BR-2.6 | `is_stale` defaults to `False` |

## BR-3: Article Editing

| Rule | Description |
|------|-------------|
| BR-3.1 | Any signed-in user can edit any article |
| BR-3.2 | Title and body validation rules (BR-2.1, BR-2.2) apply on edit |
| BR-3.3 | `updated_at` is set to current timestamp on every edit |
| BR-3.4 | An EditLog entry is created for every edit (editor_id + timestamp) |
| BR-3.5 | The original author_id is never changed |

## BR-4: Tag Management

| Rule | Description |
|------|-------------|
| BR-4.1 | Tag names are trimmed and stored lowercase |
| BR-4.2 | Empty/whitespace-only tag names are silently ignored |
| BR-4.3 | If a tag with the same name exists, reuse it (no duplicates) |
| BR-4.4 | On article edit, tags are synced: new tags added, removed tags unlinked |
| BR-4.5 | Tag name max length: 50 characters |
| BR-4.6 | Tags are added dynamically via "Add tag" button (HTMX) |

## BR-5: Search

| Rule | Description |
|------|-------------|
| BR-5.1 | Text search matches against article title AND body (SQL LIKE, case-insensitive) |
| BR-5.2 | Tag filter matches articles that have the specified tag |
| BR-5.3 | Text search + tag filter can be combined (AND logic) |
| BR-5.4 | Empty search query returns all articles (optionally filtered by tag) |
| BR-5.5 | Results ordered by `updated_at` descending (most recently updated first) |
| BR-5.6 | Live search triggers on keyup with 300ms debounce |

## BR-6: Stale Flagging

| Rule | Description |
|------|-------------|
| BR-6.1 | Any signed-in user can flag any article as stale |
| BR-6.2 | Any signed-in user can remove the stale flag |
| BR-6.3 | Toggle is a single action (flag ↔ unflag) |
| BR-6.4 | Stale articles display a warning banner but remain fully accessible |
| BR-6.5 | Stale toggle uses HTMX partial swap (no full page reload) |

## BR-7: Article Listing

| Rule | Description |
|------|-------------|
| BR-7.1 | Home page lists all articles ordered by `created_at` descending |
| BR-7.2 | Each card shows: title, author name, created date, tags, stale indicator |
| BR-7.3 | Clicking a tag filters the listing to that tag |

## BR-8: Markdown Rendering

| Rule | Description |
|------|-------------|
| BR-8.1 | Markdown is rendered server-side to HTML |
| BR-8.2 | Rendered HTML must be sanitised to prevent XSS (strip dangerous tags/attributes) |
| BR-8.3 | Preview toggle uses HTMX to fetch rendered HTML without saving |

## BR-9: Validation Summary

| Field | Rule | Error Message |
|-------|------|---------------|
| User name | Non-empty after trim | "Name is required" |
| Article title | Non-empty, max 200 chars | "Title is required" / "Title must be 200 characters or fewer" |
| Article body | Non-empty, max 50,000 chars | "Body is required" / "Body must be 50,000 characters or fewer" |
| Tag name | Max 50 chars, trimmed | Silently ignored if empty |
