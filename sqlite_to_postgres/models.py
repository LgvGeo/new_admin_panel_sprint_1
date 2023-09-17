import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FilmWork(BaseModel):

    model_config = ConfigDict(title='film_work')

    id: uuid.UUID
    title: str
    description: Optional[str]
    creation_date: Optional[str]
    rating: Optional[float]
    type: str
    created: Optional[datetime]
    modified: Optional[datetime]


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    created: Optional[datetime]
    modified: Optional[datetime]


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    created: Optional[datetime]
    modified: Optional[datetime]


class GenreFilmWork(BaseModel):

    model_config = ConfigDict(title='genre_film_work')

    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: Optional[datetime]


class PersonFilmWork(BaseModel):

    model_config = ConfigDict(title='person_film_work')

    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: Optional[datetime]
