from flask import request
from flask_restx import Resource, Namespace

from project.container import user_service
from project.setup.api.models import user_profile, error

users_ns: Namespace = Namespace('users', description='namespace for users')


@users_ns.route('/<int:user_id>')
class SingleUserView(Resource):
    @staticmethod
    @users_ns.response(404, 'Not found', error)
    @users_ns.marshal_with(user_profile, code=200, description='OK')
    def get(user_id: int):
        user: dict = user_service.get_user_by_id(user_id)
        return user, 200


@users_ns.route('/')
class AllUsersView(Resource):
    @staticmethod
    def post():
        request_body = request.json
        user_service.post_new_user(**request_body)
        return None, 201
