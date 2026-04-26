# Frontend Components — Team Knowledge Base

## Layout: `base.html`

- Shared layout wrapper for all pages
- **Nav bar**: App name/logo, link to home, signed-in user name, sign-out link
- **HTMX script**: Loaded from CDN in `<head>`
- **CSS**: Link to `/static/style.css`
- **Content block**: `{% block content %}{% endblock %}`

---

## Page: Sign In (`auth/signin.html`)

| Element | Type | Notes |
|---------|------|-------|
| Name input | `<input type="text" name="name">` | Required, autofocus |
| Submit button | `<button type="submit">` | "Sign In" |
| Error message | Conditional `<div>` | Shown if validation fails |

**Form action**: `POST /signin`

---

## Page: Article Listing (`articles/list.html`)

| Element | Type | Notes |
|---------|------|-------|
| Search input | `<input type="search">` | `hx-get="/search" hx-trigger="keyup changed delay:300ms" hx-target="#article-list"` |
| Active tag filter | Badge with clear button | Shows current tag filter if active |
| New article button | `<a href="/articles/new">` | Visible when signed in |
| Article list container | `<div id="article-list">` | Target for HTMX swaps |
| Article cards | Included via partial | Each card: title, author, date, tags, stale badge |

---

## Partial: Article List (`partials/article_list.html`)

Rendered by both full page load and HTMX search responses.

| Element | Type | Notes |
|---------|------|-------|
| Article card (repeated) | `<div class="article-card">` | One per article |
| Card → Title | `<a href="/articles/{id}">` | Link to detail |
| Card → Author | `<span>` | "by {author name}" |
| Card → Date | `<span>` | Formatted `created_at` |
| Card → Tags | `<a>` per tag | `hx-get="/search?tag={name}" hx-target="#article-list"` |
| Card → Stale badge | Conditional `<span class="stale-badge">` | "⚠ Stale" if `is_stale` |

---

## Page: Article Detail (`articles/detail.html`)

| Element | Type | Notes |
|---------|------|-------|
| Title | `<h1>` | |
| Stale banner | `<div id="stale-banner">` | Warning banner if `is_stale`, includes toggle button |
| Stale toggle button | `<button>` | `hx-post="/articles/{id}/stale" hx-target="#stale-banner" hx-swap="outerHTML"` |
| Rendered body | `<div class="article-body">` | Server-rendered markdown HTML (sanitised) |
| Tags | `<a>` per tag | Clickable, triggers tag filter |
| Author + date | `<span>` | "by {author} on {date}" |
| Edit button | `<a href="/articles/{id}/edit">` | |
| Edit log section | `<div>` | List of edit events (editor + timestamp), most recent first |

---

## Page: Article Form (`articles/form.html`)

Used for both create and edit (pre-filled in edit mode).

| Element | Type | Notes |
|---------|------|-------|
| Title input | `<input type="text" name="title" maxlength="200">` | Required |
| Body textarea | `<textarea name="body" maxlength="50000">` | Required |
| Preview toggle | `<button type="button">` | Toggles between edit/preview mode |
| Preview area | `<div id="preview-area">` | `hx-post="/articles/preview" hx-trigger="click from:#preview-btn" hx-target="#preview-area"` |
| Tag fields container | `<div id="tag-fields">` | Dynamic tag input fields |
| Tag input (repeated) | `<input type="text" name="tags" maxlength="50">` + remove button | One per tag |
| Add tag button | `<button type="button">` | `hx-get="/articles/tag-field" hx-target="#tag-fields" hx-swap="beforeend"` |
| Submit button | `<button type="submit">` | "Save Article" |
| Validation errors | Conditional `<div>` per field | Shown server-side on validation failure |

**Form action**: `POST /articles` (create) or `POST /articles/{id}/edit` (edit)

---

## Partial: Stale Banner (`partials/stale_banner.html`)

| Element | Type | Notes |
|---------|------|-------|
| Banner wrapper | `<div id="stale-banner">` | |
| Warning text | `<p>` | "⚠ This article may be outdated. Verify before relying on it." (only if stale) |
| Toggle button | `<button>` | "Flag as stale" or "Remove stale flag" depending on state |

---

## Partial: Preview (`partials/preview.html`)

| Element | Type | Notes |
|---------|------|-------|
| Rendered HTML | `<div class="markdown-preview">` | Sanitised HTML from markdown rendering |

---

## Partial: Tag Field (`partials/tag_field.html`)

Single tag input field appended dynamically.

| Element | Type | Notes |
|---------|------|-------|
| Tag input | `<input type="text" name="tags" maxlength="50">` | |
| Remove button | `<button type="button" onclick="this.parentElement.remove()">` | "✕" |

---

## HTMX Interaction Summary

| Interaction | Trigger | Endpoint | Target | Swap |
|-------------|---------|----------|--------|------|
| Live search | `keyup changed delay:300ms` | `GET /search?q=...` | `#article-list` | `innerHTML` |
| Tag filter | `click` on tag | `GET /search?tag=...` | `#article-list` | `innerHTML` |
| Toggle stale | `click` button | `POST /articles/{id}/stale` | `#stale-banner` | `outerHTML` |
| Markdown preview | `click` preview btn | `POST /articles/preview` | `#preview-area` | `innerHTML` |
| Add tag field | `click` add btn | `GET /articles/tag-field` | `#tag-fields` | `beforeend` |
