from flask_restx import Resource, Namespace

from project.container import genre_service
from project.setup.api.models import genre, error
from project.setup.api.parsers import page_parser

genres_ns: Namespace = Namespace('genres', description='namespace for genres')


@genres_ns.route('/')
class AllGenresView(Resource):
    """
    GET: implements get request for all genres
    """

    @staticmethod
    @genres_ns.expect(page_parser)
    @genres_ns.marshal_with(genre, as_list=True, code=200, description='OK')
    def get():
        all_genres: list[dict] = genre_service.get_all_genres(**page_parser.parse_args())
        return all_genres, 200


@genres_ns.route('/<int:genre_id>')
class SingleGenreView(Resource):
    """
    GET: implements get request for exact genre by its id
    """

    @staticmethod
    @genres_ns.response(404, 'Not found', error)
    @genres_ns.marshal_with(genre, code=200, description='OK')
    def get(genre_id: int):
        current_genre: dict = genre_service.get_genre_by_id(genre_id)
        return current_genre, 200
