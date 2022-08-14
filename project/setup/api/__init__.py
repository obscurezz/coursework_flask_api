from flask_restx import Api
from project.views import movies_ns, genres_ns, directors_ns

api = Api(
    title='Coursework_3_API',
    version='1.0',
    description='All namespaces of project into one API'
)

api.add_namespace(genres_ns)
api.add_namespace(directors_ns)
api.add_namespace(movies_ns)
