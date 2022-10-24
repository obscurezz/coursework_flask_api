from flask_restx import Resource, Namespace

from project.container import favorite_service, user_service
from project.setup.api.models import error, favorite_model
from project.tools.decorators import auth_required

favorites_ns: Namespace = Namespace('favorites/movies', description='namespace for favorites')


@favorites_ns.route('/<int:movie_id>')
class FavoritesView(Resource):
    @staticmethod
    @favorites_ns.response(404, 'Not found', error)
    @favorites_ns.response(401, 'Not authorized', error)
    @favorites_ns.marshal_with(favorite_model, code=200, description='OK')
    @auth_required
    def post(username, movie_id: int):
        """
        adds new favorite
        """
        user: dict = user_service.get_user_by_email_and_password(email=username)
        user_id: int = user['id']

        new_favorite = favorite_service.post_new_favorite(user_id, movie_id)
        return new_favorite, 201

    @staticmethod
    @favorites_ns.response(404, 'Not found', error)
    @favorites_ns.response(401, 'Not authorized', error)
    @auth_required
    def delete(username, movie_id: int):
        """
        deletes the favorite
        """
        user: dict = user_service.get_user_by_email_and_password(email=username)
        user_id: int = user['id']

        favorite_service.delete_favorite(user_id, movie_id)
        return "", 204
