from pydantic import BaseModel, field_validator


class ArticleForm(BaseModel):
    title: str
    body: str
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title is required")
        if len(v) > 200:
            raise ValueError("Title must be 200 characters or fewer")
        return v

    @field_validator("body")
    @classmethod
    def body_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Body is required")
        if len(v) > 50_000:
            raise ValueError("Body must be 50,000 characters or fewer")
        return v

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: list[str]) -> list[str]:
        cleaned = []
        for tag in v:
            tag = tag.strip().lower()
            if tag and len(tag) <= 50:
                cleaned.append(tag)
        return cleaned
