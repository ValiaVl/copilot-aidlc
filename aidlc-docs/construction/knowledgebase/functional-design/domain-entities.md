# Domain Entities — Team Knowledge Base

## Entity: User

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | Integer | PK, auto-increment | |
| `name` | String(100) | Unique, not null | Stored lowercase for case-insensitive matching |
| `created_at` | DateTime | Not null, default=now | Account creation timestamp |

**Relationships**:
- One-to-many → Article (as author)
- One-to-many → EditLog (as editor)

---

## Entity: Article

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | Integer | PK, auto-increment | |
| `title` | String(200) | Not null, max 200 chars | |
| `body` | Text | Not null, max 50,000 chars | Raw markdown content |
| `author_id` | Integer | FK → User.id, not null | Creator |
| `is_stale` | Boolean | Not null, default=False | Stale flag |
| `created_at` | DateTime | Not null, default=now | |
| `updated_at` | DateTime | Not null, default=now, auto-update | Updated on every edit |

**Relationships**:
- Many-to-one → User (author)
- Many-to-many → Tag (via ArticleTag)
- One-to-many → EditLog

---

## Entity: Tag

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | Integer | PK, auto-increment | |
| `name` | String(50) | Unique, not null | Stored lowercase, trimmed |

**Relationships**:
- Many-to-many → Article (via ArticleTag)

---

## Entity: ArticleTag (Association Table)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `article_id` | Integer | PK, FK → Article.id | Composite primary key |
| `tag_id` | Integer | PK, FK → Tag.id | Composite primary key |

**Cascade**: Delete ArticleTag rows when Article is deleted.

---

## Entity: EditLog

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | Integer | PK, auto-increment | |
| `article_id` | Integer | FK → Article.id, not null | |
| `editor_id` | Integer | FK → User.id, not null | |
| `edited_at` | DateTime | Not null, default=now | |

**Relationships**:
- Many-to-one → Article
- Many-to-one → User (editor)

---

## Entity Relationship Diagram

```
User (id, name, created_at)
  |
  |-- 1:N --> Article (id, title, body, author_id, is_stale, created_at, updated_at)
  |               |
  |               |-- M:N --> Tag (id, name)  [via ArticleTag]
  |               |
  |               |-- 1:N --> EditLog (id, article_id, editor_id, edited_at)
  |
  |-- 1:N --> EditLog (via editor_id)
```
