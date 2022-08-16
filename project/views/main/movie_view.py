from flask_restx import Resource, Namespace

from project.container import movie_service
from project.setup.api.models import error, movie
from project.setup.api.parsers import movie_status_and_page_parser

movies_ns: Namespace = Namespace('movies', description='namespace for movies')


@movies_ns.route('/')
class AllMoviesView(Resource):
    """
    GET: implements GET-method for /movies
    POST: implements POST-method to add new object to database (isn't done yet)
    """

    @staticmethod
    @movies_ns.expect(movie_status_and_page_parser)
    @movies_ns.marshal_with(movie, as_list=True, code=200, description='OK')
    def get():
        all_movies: list[dict] = movie_service.get_all_movies(**movie_status_and_page_parser.parse_args())
        return all_movies, 200


@movies_ns.route('/<int:movie_id>')
class SingleMovieView(Resource):
    """
    GET: implements GET-method for /movies/... where ... is ID of object
    PUT: implements PUT-method to fully update object in database (isn't done yet)
    DELETE: implements DELETE-method to delete object from database (isn't done yet)
    """

    @staticmethod
    @movies_ns.response(404, 'Not found', error)
    @movies_ns.marshal_with(movie, code=200, description='OK')
    def get(movie_id: int):
        current_movie: dict = movie_service.get_movie_by_id(movie_id)
        return current_movie, 200
