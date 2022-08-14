from flask_restx import Resource, Namespace
from flask import jsonify

from project.orm_models import Director

from project.container import director_service
from project.models import DirectorModel


directors_ns: Namespace = Namespace('directors', description='namespace for directors')


@directors_ns.route('/')
class AllDirectorsView(Resource):
    pass
    """
    GET: implements get request for all directors
    """
#     @staticmethod
#     def get():
#         all_directors: list[Director] = director_service.get_all_directors()
#         return directors_model.dump(all_directors), 200
#
#
# @directors_ns.route('/<int:did>')
# class SingleDirectorView(Resource):
#     """
#     GET: implements get request for exact director by its id
#     """
#     @staticmethod
#     def get(did: int):
#         current_director: Director = director_service.get_director_by_id(did)
#         try:
#             return director_model.dump(current_director)
#         except Exception as e:
#             return jsonify({'Exception': e}), 500
