from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from project.setup.db.base_model import BaseORM


class Genre(BaseORM):
    __tablename__ = 'genres'

    name = Column(VARCHAR(100), unique=True, nullable=False)


class Director(BaseORM):
    __tablename__ = 'directors'

    name = Column(VARCHAR(200), unique=True, nullable=False)


class Movie(BaseORM):
    __tablename__ = 'movies'

    title = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(255), default="No description", nullable=False)
    trailer = Column(VARCHAR(255))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, nullable=False)
    director_id = Column(Integer, nullable=False)

    genre = relationship("Genre")
    director = relationship("Director")

    __table_args__ = (
        ForeignKeyConstraint((genre_id,), (Genre.id,), onupdate='CASCADE', ondelete='CASCADE'),
        ForeignKeyConstraint((director_id,), (Director.id,), onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint("trailer REGEXP '(http|https)://'"),
        CheckConstraint("year > 1700"),
        CheckConstraint("rating BETWEEN 0.0 AND 10.0"),
    )


class User(BaseORM):
    __tablename__ = 'users'

    email = Column(VARCHAR(200), unique=True, nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    first_name = Column(VARCHAR(100), nullable=False)
    last_name = Column(VARCHAR(100), nullable=False)
    favorite_genre = Column(VARCHAR(100))

    __table_args__ = (
        CheckConstraint("email LIKE '%___@___%.__%'"),
    )


class UserFavorites(BaseORM):
    __tablename__ = 'user_favorites'

    user_id = Column(Integer, nullable=False)
    movie_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint((user_id,), (User.id,), onupdate='CASCADE', ondelete='CASCADE'),
        ForeignKeyConstraint((movie_id,), (Movie.id,), onupdate='CASCADE', ondelete='CASCADE'),
    )
