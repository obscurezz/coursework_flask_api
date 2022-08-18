from flask_restx import Resource, Namespace

from project.container import director_service
from project.setup.api.models import director, error
from project.setup.api.parsers import page_parser

directors_ns: Namespace = Namespace('directors', description='namespace for directors')


@directors_ns.route('/')
class AllDirectorsView(Resource):
    """
    GET: implements get request for all directors
    """

    @staticmethod
    @directors_ns.expect(page_parser)
    @directors_ns.marshal_with(director, as_list=True, code=200, description='OK')
    def get():
        """
        all directors with pagination
        """
        all_directors: list[dict] = director_service.get_all_directors(**page_parser.parse_args())
        return all_directors, 200


@directors_ns.route('/<int:director_id>')
class SingleDirectorView(Resource):
    """
    GET: implements get request for exact director by its id
    """

    @staticmethod
    @directors_ns.response(404, 'Not found', error)
    @directors_ns.marshal_with(director, code=200, description='OK')
    def get(director_id: int):
        """
        exact director by its id
        """
        current_director: dict = director_service.get_director_by_id(director_id)
        return current_director, 200
