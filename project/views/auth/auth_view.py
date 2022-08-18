from flask_restx import Resource, Namespace

from project.container import auth_service, user_service
from project.setup.api.models import token, error
from project.setup.api.parsers import auth_parser, tokens_parser, new_user_parser

auth_ns = Namespace('auth', description='namespace for authorization')


@auth_ns.route('/login')
class LoginAuthView(Resource):
    @staticmethod
    @auth_ns.expect(auth_parser)
    @auth_ns.marshal_with(token, code=200, description='OK')
    @auth_ns.response(code=400, description='Bad request', model=error)
    def post():
        tokens = auth_service._generate_tokens(**auth_parser.parse_args())
        return tokens, 201

    @staticmethod
    @auth_ns.expect(tokens_parser)
    @auth_ns.marshal_with(token, code=200, description='OK')
    def put():
        return auth_service._approve_refresh_token(tokens_parser.parse_args()['refresh_token']), 201


@auth_ns.route('/register')
class RegisterAuthView(Resource):
    @staticmethod
    @auth_ns.expect(new_user_parser)
    @auth_ns.response(code=201, description='Created user')
    @auth_ns.response(code=400, description='Bad request', model=error)
    @auth_ns.response(code=409, description='Already exists', model=error)
    def post():
        new_user = user_service.post_new_user(**new_user_parser.parse_args())
        return new_user, 201
