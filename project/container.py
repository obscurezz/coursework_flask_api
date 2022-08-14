from project.dao import MovieDAO, GenreDAO, DirectorDAO
from project.services import MovieService, GenreService, DirectorService
from project.setup.db import db

movie_dao = MovieDAO(db_session=db.session)
movie_service = MovieService(dao=movie_dao)

genre_dao = GenreDAO(db_session=db.session)
genre_service = GenreService(dao=genre_dao)

director_dao = DirectorDAO(db_session=db.session)
director_service = DirectorService(dao=director_dao)
