from flask_restx import Resource, Namespace
from flask import jsonify

from project.orm_models import Genre

from project.container import genre_service
from project.models import GenreModel

genres_ns: Namespace = Namespace('genres', description='namespace for genres')


@genres_ns.route('/')
class AllGenresView(Resource):
    """
    GET: implements get request for all genres
    """
    @staticmethod
    def get():
        all_genres: list[Genre] = genre_service.get_all_genres(page=1)
        validated_genres: list[dict] = [GenreModel.from_orm(genre).dict() for genre in all_genres]
        return validated_genres, 200


@genres_ns.route('/<int:genre_id>')
class SingleGenreView(Resource):
    """
    GET: implements get request for exact genre by its id
    """
    @staticmethod
    def get(genre_id: int):
        current_genre: Genre = genre_service.get_genre_by_id(genre_id)
        validated_genre: dict = GenreModel.from_orm(current_genre).dict()
        return validated_genre, 200
