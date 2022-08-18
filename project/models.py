from typing import Optional

from pydantic import BaseModel, EmailStr, Field


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


class MovieModel(BaseModel):
    id: Optional[int]
    title: str
    description: str
    trailer: str = Field(regex='(http|https)://', description='should be a link')
    year: int = Field(gt=1700)
    rating: float = Field(ge=0, le=10)
    genre_id: int
    director_id: int

    director: DirectorModel | None
    genre: GenreModel | None

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    id: Optional[int]
    email: EmailStr
    password: str
        # = Field(regex='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
        #                   description='8 chars, must contain at least 1 digit, 1 upper, 1 lower, 1 special')
    first_name: str
    last_name: str
    favorite_genre: GenreModel | None

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str = Field(regex='(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)')
    refresh_token: str = Field(regex='(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)')


class UserFavoritesModel(BaseModel):
    id: int | None
    user_id: int
    movie_id: int

    class Config:
        orm_mode = True
