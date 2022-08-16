from typing import Optional
from pydantic import BaseModel, EmailStr


class MovieModel(BaseModel):
    id: Optional[int]
    title: str
    description: str
    trailer: str
    year: int
    rating: float
    genre_id: int
    director_id: int

    class Config:
        orm_mode = True


class GenreModel(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True


class DirectorModel(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    id: Optional[int]
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    favorite_genre: str | None

    class Config:
        orm_mode = True
