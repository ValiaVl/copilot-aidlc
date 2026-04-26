# User Stories — Team Knowledge Base

**Persona**: Team Member
**Breakdown**: Persona-Based (single persona)
**Acceptance Criteria**: High-level bullet points
**Priority/Sizing**: Not included

---

## Sign-In & Identity

### US-1: Sign In
**As a** Team Member, **I want to** sign in by entering my name, **so that** the system knows who I am without needing a password.

**Acceptance Criteria:**
- I can enter my display name on a sign-in page
- The system recognises me if I've signed in before (case-insensitive)
- A new user record is created automatically for first-time names
- I stay signed in across page loads via a session cookie

### US-2: Sign Out
**As a** Team Member, **I want to** sign out, **so that** I can end my session.

**Acceptance Criteria:**
- A sign-out button is visible when I'm signed in
- Clicking it ends my session and returns me to the sign-in page

---

## Article Authoring

### US-3: Create Article
**As a** Team Member, **I want to** create a new documentation article, **so that** I can record knowledge for the team.

**Acceptance Criteria:**
- I can enter a title, markdown body, and optional tags
- The article is saved with my name as author and the current timestamp
- After saving, I can see the rendered article

### US-4: Toggle Markdown Preview
**As a** Team Member, **I want to** toggle between editing markdown and viewing rendered HTML, **so that** I can preview how the article will look.

**Acceptance Criteria:**
- An edit/preview toggle is available on the article editor
- Preview mode renders the markdown as HTML
- Switching back to edit mode preserves my content

---

## Article Editing

### US-5: Edit Any Article
**As a** Team Member, **I want to** edit any article, **so that** I can improve or correct existing knowledge.

**Acceptance Criteria:**
- An edit button is available on any article detail page
- I can modify the title, body, and tags
- Saving records my name and timestamp in the edit log

### US-6: View Edit History
**As a** Team Member, **I want to** see who edited an article and when, **so that** I know how recently it was updated.

**Acceptance Criteria:**
- The article detail page shows a list of edit events (editor name + timestamp)
- The list is ordered most recent first

---

## Tagging

### US-7: Add Tags to Article
**As a** Team Member, **I want to** add tags when creating or editing an article, **so that** it's easier to find later.

**Acceptance Criteria:**
- I can type one or more free-text tags when creating or editing
- Tags are displayed on the article card and detail page

### US-8: Filter by Tag
**As a** Team Member, **I want to** click a tag to filter the article list, **so that** I can see all articles on a topic.

**Acceptance Criteria:**
- Clicking a tag on any article filters the listing to that tag
- The active tag filter is visually indicated
- I can clear the filter to see all articles again

---

## Search

### US-9: Search Articles
**As a** Team Member, **I want to** search articles by text, **so that** I can quickly find what I need.

**Acceptance Criteria:**
- A search box is available on the article listing page
- Typing a query filters articles matching title or body text
- Results update as I type or on submit

### US-10: Combined Search and Tag Filter
**As a** Team Member, **I want to** combine text search with a tag filter, **so that** I can narrow results precisely.

**Acceptance Criteria:**
- I can apply both a text search and a tag filter at the same time
- Results satisfy both the text query and the selected tag(s)

---

## Stale Flagging

### US-11: Flag Article as Stale
**As a** Team Member, **I want to** flag an article as stale, **so that** others know it may be outdated.

**Acceptance Criteria:**
- A "Flag as stale" button is available on the article detail page
- Flagged articles show a visual warning banner
- The article remains fully readable

### US-12: Remove Stale Flag
**As a** Team Member, **I want to** remove the stale flag from an article, **so that** I can indicate it's been verified.

**Acceptance Criteria:**
- An "Unflag" button is available on stale articles
- Removing the flag hides the warning banner

---

## Article Listing & Navigation

### US-13: View All Articles
**As a** Team Member, **I want to** see all articles on the home page, **so that** I can browse recent knowledge.

**Acceptance Criteria:**
- The home page lists all articles, most recent first
- Each card shows title, author, date, tags, and stale indicator (if applicable)

### US-14: View Article Detail
**As a** Team Member, **I want to** click an article to read it, **so that** I can see the full rendered content.

**Acceptance Criteria:**
- Clicking an article card opens the detail/read view
- The detail page shows rendered markdown, author, date, tags, edit log, and stale banner (if applicable)

---

## INVEST Compliance

| Story | I | N | V | E | S | T |
|-------|---|---|---|---|---|---|
| US-1 Sign In | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-2 Sign Out | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-3 Create Article | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-4 Toggle Preview | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-5 Edit Article | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-6 View Edit History | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-7 Add Tags | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-8 Filter by Tag | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-9 Search Articles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-10 Combined Search+Tag | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-11 Flag Stale | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-12 Remove Stale | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-13 View All Articles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| US-14 View Article Detail | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legend**: I=Independent, N=Negotiable, V=Valuable, E=Estimable, S=Small, T=Testable
