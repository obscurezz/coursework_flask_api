from flask_restx import Resource, Namespace

from project.container import user_service
from project.setup.api.models import user_profile, error
from project.setup.api.parsers import update_user_parser, change_password_parser
from project.tools.decorators import auth_required

users_ns: Namespace = Namespace('user', description='namespace for users')


@users_ns.route('/')
class SingleUserView(Resource):
    @staticmethod
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @users_ns.marshal_with(user_profile, code=200, description='OK')
    @auth_required
    def get(email):
        """
        returns user info for authorized user
        """
        user: dict = user_service.get_user_by_email_and_password(email=email)
        return user, 200

    @staticmethod
    @users_ns.expect(update_user_parser)
    @users_ns.response(code=201, description='User updated')
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @auth_required
    def patch(email):
        """
        updates user info for authorized user
        """
        user: dict = user_service.get_user_by_email_and_password(email=email)
        pk = user['id']

        user_service.patch_user_by_id(pk, **update_user_parser.parse_args())
        return "", 201


@users_ns.route('/password')
class PasswordUserView(Resource):
    @staticmethod
    @users_ns.expect(change_password_parser)
    @users_ns.response(code=201, description='User password updated')
    @users_ns.response(404, 'Not found', error)
    @users_ns.response(401, 'Not authorized', error)
    @auth_required
    def put(email):
        """
        changes user password for authorized user
        """
        user: dict = user_service.get_user_by_email_and_password(email=email)
        pk = user['id']

        user_service.put_user_new_password(pk, **change_password_parser.parse_args())
        return "", 201
