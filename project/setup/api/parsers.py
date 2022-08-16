from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

movie_status_and_page_parser: RequestParser = page_parser.copy()
movie_status_and_page_parser.add_argument(name='status', type=str, location='args', choices=('NEW',), required=False)
