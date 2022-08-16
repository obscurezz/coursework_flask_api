from pydantic import BaseModel, EmailStr


class MovieModel(BaseModel):
    id: int
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
    id: int
    name: str

    class Config:
        orm_mode = True


class DirectorModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    id: int
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    favorite_genre: str | None

    class Config:
        orm_mode = True
