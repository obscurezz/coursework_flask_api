from flask_restx import Resource, Namespace
from flask import request, jsonify

from project.orm_models import Movie

from project.container import movie_service
from project.models import MovieModel


movies_ns: Namespace = Namespace('movies', description='namespace for movies')
#
# movie_model = MovieModel()
# movies_model = MovieModel(many=True)


@movies_ns.route('/')
class AllMoviesView(Resource):
    """
    GET: implements GET-method for /movies
    POST: implements POST-method to add new object to database
    """
    @staticmethod
    def get():
        all_movies: list[Movie] = movie_service.get_all_movies()
        validated_movies = [MovieModel.from_orm(movie) for movie in all_movies]
        return validated_movies, 200
