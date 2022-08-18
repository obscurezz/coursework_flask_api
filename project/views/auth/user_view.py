from flask import url_for
from flask_restx import Resource, Namespace

from project.container import user_service
from project.setup.api.models import user_profile, error
from project.tools.decorators import auth_required
from project.setup.api.parsers import update_user_parser, change_password_parser

users_ns: Namespace = Namespace('user', description='namespace for users')


@users_ns.route('/')
class SingleUserView(Resource):
    @staticmethod
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @users_ns.marshal_with(user_profile, code=200, description='OK')
    @auth_required
    def get(current_user):
        user: dict = user_service.get_user_by_email_and_password(email=current_user['username'])
        return user, 200

    @staticmethod
    @users_ns.expect(update_user_parser)
    @users_ns.response(code=201, description='User updated', headers={'Location': 'URL of updated user'})
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @auth_required
    def patch(current_user):
        user: dict = user_service.get_user_by_email_and_password(email=current_user['username'])
        pk = user['id']

        user_service.patch_user_by_id(pk, **update_user_parser.parse_args())
        return "", 201, {'Location': url_for(f'/user/')}


@users_ns.route('/password')
class PasswordUserView(Resource):
    @staticmethod
    @users_ns.expect(change_password_parser)
    @users_ns.response(code=201, description='User password updated', headers={'Location': 'URL of updated user'})
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @auth_required
    def put(current_user):
        user: dict = user_service.get_user_by_email_and_password(email=current_user['username'])
        pk = user['id']

        user_service.put_user_new_password(pk, **change_password_parser.parse_args())
        return "", 201, {'Location': url_for(f'/user/')}
