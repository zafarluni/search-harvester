"""
Pydantic models for API responses.
"""

from pydantic import BaseModel, Field


class ArticleResult(BaseModel):
    source: str
    title: str
    content: str
    word_count: int = Field(..., ge=0, description="The number of words, must be >= 0")
