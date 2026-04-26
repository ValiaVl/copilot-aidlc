# Requirements Document — Favorites Feature

## Intent Analysis

- **User Request**: Add a favorites feature so users can mark any article as a favorite, see a "My Favorites" view listing only favorited articles, and toggle the favorite status with one click from both the listing page and the article detail page.
- **Request Type**: New Feature (brownfield enhancement)
- **Scope Estimate**: Multiple Components (model, service, routes, templates, database)
- **Complexity Estimate**: Simple-to-Moderate
- **Depth Level**: Standard

---

## Functional Requirements

### FR-FAV-1: Favorite Toggle
- Any signed-in user can mark any article as a favorite
- Any signed-in user can remove the favorite mark (un-favorite)
- Toggle is performed with **one click** — no confirmation dialog
- Toggle uses HTMX for instant UI update without full page reload
- The toggle is represented as a **heart icon**: ♥ (filled) when favorited, ♡ (outline) when not

### FR-FAV-2: Favorite Toggle on Listing Page
- Each article card on the home listing page displays a heart icon toggle
- Clicking the heart toggles the favorite status for the current user
- The icon updates immediately via HTMX swap

### FR-FAV-3: Favorite Toggle on Detail Page
- The article detail page displays a heart icon toggle
- Clicking the heart toggles the favorite status for the current user
- The icon updates immediately via HTMX swap

### FR-FAV-4: Favorites Count
- Each article displays the **total number of users** who have favorited it
- The count is visible on both the listing page (article cards) and the detail page
- The count updates when the current user toggles their favorite

### FR-FAV-5: "My Favorites" View
- A dedicated **filter toggle** on the home/listing page allows the user to switch between "All articles" and "My Favorites"
- When "My Favorites" is active, only articles favorited by the current user are shown
- Favorited articles are sorted by **most recently favorited first**
- The filter is accessible only to signed-in users

### FR-FAV-6: Signed-In Requirement
- Only signed-in users can favorite/un-favorite articles
- The heart icon is not shown (or is non-interactive) for users who are not signed in
- The "My Favorites" filter is hidden for users who are not signed in

---

## Non-Functional Requirements

- Same tech stack as existing app (FastAPI, HTMX, SQLAlchemy, SQLite, Jinja2)
- No new dependencies required
- Performance: favorite toggle should respond in under 200ms (local development)

---

## Data Model Extension

| Entity | Key Fields | Notes |
|--------|-----------|-------|
| **Favorite** | id, user_id (FK → User), article_id (FK → Article), created_at | Unique constraint on (user_id, article_id) |

---

## Out of Scope
- Favoriting from search results (search uses existing partial, can be added later)
- Favorite notifications
- Exporting favorites list
- Favoriting tags or users
