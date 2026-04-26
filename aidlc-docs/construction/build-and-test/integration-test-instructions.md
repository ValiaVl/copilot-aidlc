# Integration Test Instructions — Team Knowledge Base

## Purpose
Test complete user workflows end-to-end through the running application.

## Setup

```bash
# Start the application
uv run uvicorn app.main:app --reload
```

## Manual Integration Test Scenarios

### Scenario 1: Sign In → Create Article → View
1. Open http://127.0.0.1:8000/signin
2. Enter a name (e.g., "Alice") and click "Sign In"
3. Click "+ New Article"
4. Enter title: "Test Article", body: "Some **markdown** content"
5. Click "+ Add Tag", enter "test"
6. Click "Save Article"
7. **Expected**: Redirected to article detail page showing rendered markdown, author "alice", and tag "test"

### Scenario 2: Edit Article → View Edit Log
1. From the article detail page, click "Edit"
2. Change the title and body
3. Click "Save Article"
4. **Expected**: Article updated, edit history shows the editor name and timestamp

### Scenario 3: Stale Flagging
1. On any article detail page, click "Flag as stale"
2. **Expected**: Yellow warning banner appears ("This article may be outdated"), button changes to "Remove stale flag"
3. Click "Remove stale flag"
4. **Expected**: Banner disappears, button reverts to "Flag as stale"

### Scenario 4: Live Search
1. Go to the home page (/)
2. Type "test" in the search box
3. **Expected**: Article list filters dynamically after ~300ms delay

### Scenario 5: Tag Filtering
1. Click a tag on any article card
2. **Expected**: Article list filters to show only articles with that tag
3. Click "✕" to clear the filter
4. **Expected**: All articles shown again

### Scenario 6: Markdown Preview Toggle
1. Create or edit an article
2. Enter markdown in the body (e.g., `# Heading\n**bold** text`)
3. Click "Preview"
4. **Expected**: Rendered HTML shown instead of textarea
5. Click "Edit"
6. **Expected**: Textarea restored with original markdown

### Scenario 7: Multiple Users
1. Sign out and sign in as a different name (e.g., "Bob")
2. Edit an article created by Alice
3. **Expected**: Edit succeeds, edit log shows "bob" as editor

## Cleanup
- Delete `knowledgebase.db` to reset all data
- Restart the application
