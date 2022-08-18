from project.dao import MovieDAO, GenreDAO, DirectorDAO, UserDAO
from project.services import MovieService, GenreService, DirectorService, UserService, AuthService
from project.setup.db import db

movie_dao = MovieDAO(db_session=db.session)
movie_service = MovieService(dao=movie_dao)

genre_dao = GenreDAO(db_session=db.session)
genre_service = GenreService(dao=genre_dao)

director_dao = DirectorDAO(db_session=db.session)
director_service = DirectorService(dao=director_dao)

user_dao = UserDAO(db_session=db.session)
user_service = UserService(dao=user_dao)

auth_service = AuthService(user_service=user_service)
