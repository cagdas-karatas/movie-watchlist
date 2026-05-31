from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class MovieBase(BaseModel):
    title: str
    director: str | None = None
    year: int | None = None
    genre: str | None = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None
    genre: str | None = None
    watched: bool | None = None
    rating: int | None = None

    @field_validator("rating")
    @classmethod
    def rating_must_be_1_to_10(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 10):
            raise ValueError("rating must be between 1 and 10")
        return v


class MovieResponse(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    watched: bool
    rating: int | None = None
    added_at: datetime
    watched_at: datetime | None = None


class StatsResponse(BaseModel):
    total: int
    watched_count: int
    unwatched_count: int
    avg_rating: float | None
