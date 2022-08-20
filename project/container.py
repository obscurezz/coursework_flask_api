from project.dao import MovieDAO, GenreDAO, DirectorDAO, UserDAO, FavoriteDAO
from project.services import MovieService, GenreService, DirectorService, UserService, AuthService, FavoriteService

# movies
movie_dao = MovieDAO()
movie_service = MovieService(dao=movie_dao)
# genres
genre_dao = GenreDAO()
genre_service = GenreService(dao=genre_dao)
# directors
director_dao = DirectorDAO()
director_service = DirectorService(dao=director_dao)
# users
user_dao = UserDAO()
user_service = UserService(dao=user_dao)
# authorization
auth_service = AuthService(user_service=user_service)
# favorites
favorite_dao = FavoriteDAO()
favorite_service = FavoriteService(dao=favorite_dao)
