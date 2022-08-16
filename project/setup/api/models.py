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
