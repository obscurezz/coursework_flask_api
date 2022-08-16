from flask_restx import Resource, Namespace
from flask import request

from project.orm_models import Movie

from project.container import movie_service
from project.models import MovieModel


movies_ns: Namespace = Namespace('movies', description='namespace for movies')


@movies_ns.route('/')
class AllMoviesView(Resource):
    """
    GET: implements GET-method for /movies
    POST: implements POST-method to add new object to database
    """
    @staticmethod
    def get():
        page = request.args['page']
        status = request.args['status']

        all_movies: list[Movie] = movie_service.get_all_movies(page=1)
        validated_movies: list[dict] = [MovieModel.from_orm(movie).dict() for movie in all_movies]
        return validated_movies, 200


@movies_ns.route('/<int:movie_id>')
class SingleMovieView(Resource):
    """
    GET: implements GET-method for /movies/... where ... is ID of object
    PUT: implements PUT-method to fully update object in database
    DELETE: implements DELETE-method to delete object from database
    """
    @staticmethod
    def get(movie_id: int):
        current_movie: Movie = movie_service.get_movie_by_id(movie_id)
        validated_movie: dict = MovieModel.from_orm(current_movie).dict()
        return validated_movie, 200

