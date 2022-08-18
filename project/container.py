from project.dao import MovieDAO, GenreDAO, DirectorDAO, UserDAO, FavoriteDAO
from project.services import MovieService, GenreService, DirectorService, UserService, AuthService, FavoriteService
from project.setup.db import db
# movies
movie_dao = MovieDAO(db_session=db.session)
movie_service = MovieService(dao=movie_dao)
# genres
genre_dao = GenreDAO(db_session=db.session)
genre_service = GenreService(dao=genre_dao)
# directors
director_dao = DirectorDAO(db_session=db.session)
director_service = DirectorService(dao=director_dao)
# users
user_dao = UserDAO(db_session=db.session)
user_service = UserService(dao=user_dao)
# authorization
auth_service = AuthService(user_service=user_service)
# favorites
favorite_dao = FavoriteDAO(db_session=db.session)
favorite_service = FavoriteService(dao=favorite_dao)
