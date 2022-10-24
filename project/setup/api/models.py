from flask_restx import Model, fields

from project.setup.api import api


error: Model = api.model('Error message', {
    'message': fields.String(required=True),
    'errors': fields.Wildcard(fields.String(), required=False)
})

genre: Model = api.model('Genre', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100)
})

director: Model = api.model('Director', {
    'id': fields.Integer(required=True, example=2),
    'name': fields.String(required=True, max_length=100)
})

movie: Model = api.model('Movie', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=200),
    'description': fields.String(required=True, max_length=255),
    'trailer': fields.String(required=True, max_length=255),
    'year': fields.Integer(required=True, min=1700, example=2000),
    'rating': fields.Float(required=True, min=0.0, max=10.0, example=5.5),
    'genre': fields.Nested(genre, required=True),
    'director': fields.Nested(director, required=True)
})

user_profile: Model = api.model('User', {
    'id': fields.Integer(required=True),
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'favorite_genre': fields.String
})

token: Model = api.model('Access/Refresh token',{
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True),
})

favorite_model: Model = api.model('Favorite',{
    'id': fields.Integer(required=True),
    'user': fields.Nested(user_profile, required=True),
    'movie': fields.Nested(movie, required=True),
})
