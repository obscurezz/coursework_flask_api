from flask_restx import Resource, Namespace
from flask import request

from project.orm_models import Director

from project.container import director_service
from project.models import DirectorModel


directors_ns: Namespace = Namespace('directors', description='namespace for directors')


@directors_ns.route('/')
class AllDirectorsView(Resource):
    """
    GET: implements get request for all directors
    """
    @staticmethod
    def get():
        page: int = int(request.args.get('page'))

        all_directors: list[Director] = director_service.get_all_directors(page=page)
        validated_directors: list[dict] = [DirectorModel.from_orm(director).dict() for director in all_directors]
        return validated_directors, 200


@directors_ns.route('/<int:director_id>')
class SingleDirectorView(Resource):
    """
    GET: implements get request for exact director by its id
    """
    @staticmethod
    def get(director_id: int):
        current_director: Director = director_service.get_director_by_id(director_id)
        validated_director: dict = DirectorModel.from_orm(current_director).dict()
        return validated_director, 200
