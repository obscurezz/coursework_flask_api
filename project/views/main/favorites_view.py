from flask_restx import Resource, Namespace

from project.container import favorite_service, user_service
from project.setup.api.models import error
from project.tools.decorators import auth_required

favorites_ns: Namespace = Namespace('favorites/movies', description='namespace for favorites')


@favorites_ns.route('/<int:movie_id>')
class FavoritesView(Resource):
    @staticmethod
    @favorites_ns.response(404, 'Not found', error)
    @favorites_ns.response(401, 'Not authorized', error)
    @auth_required
    def post(username, movie_id: int):
        user: dict = user_service.get_user_by_email_and_password(email=username)
        user_id: int = user['id']

        favorite_service.post_new_favorite(user_id, movie_id)
        return "", 201

    @staticmethod
    @favorites_ns.response(404, 'Not found', error)
    @favorites_ns.response(401, 'Not authorized', error)
    @auth_required
    def delete(username, movie_id: int):
        user: dict = user_service.get_user_by_email_and_password(email=username)
        user_id: int = user['id']

        favorite_service.delete_favorite(user_id, movie_id)
        return "", 204
