# Requirements Verification Questions

Please answer each question by filling in the letter choice after the `[Answer]:` tag.

---

## Question 1
How should articles be stored (persistence layer)?

A) SQLite — single-file database, simple deployment, good for small teams
B) PostgreSQL — full relational DB, good for production and scaling
C) JSON files on disk — simplest approach, no database needed
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
Should the markdown editor include a live preview, or is a plain text area sufficient?

A) Plain text area — users type markdown, see rendered output only after saving
B) Side-by-side live preview — editor on the left, rendered preview on the right
C) Toggle preview — switch between edit and preview modes
D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 3
How should search work?

A) Simple text search — match keywords in title and body
B) Full-text search with ranking — results ordered by relevance
C) Tag-based filtering only — no free-text search
D) Both text search and tag filtering combined
E) Other (please describe after [Answer]: tag below)

[Answer]: D

## Question 4
What should happen when an article is flagged as stale?

A) Show a visual warning banner on the article, but keep it fully accessible
B) Show a warning banner AND move stale articles lower in search results
C) Show a warning banner AND require confirmation before viewing full content
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
Should there be any article history or versioning?

A) No history — edits overwrite the previous version
B) Simple edit log — track who edited and when, but no content diffs
C) Full version history — store every revision with ability to view/restore previous versions
D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 6
Are there any deployment preferences or constraints?

A) Local development only — run on localhost for now
B) Single server deployment — Docker container or similar
C) Cloud deployment — AWS, GCP, Azure, etc.
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 7: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 8: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)
B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)
C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)
D) Other (please describe after [Answer]: tag below)

[Answer]: C
