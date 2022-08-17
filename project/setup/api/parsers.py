from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

movie_status_and_page_parser: RequestParser = page_parser.copy()
movie_status_and_page_parser.add_argument(name='status', type=str, location='args', choices=('NEW',), required=False)

auth_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='email', type=email(), required=True, nullable=False)
auth_parser.add_argument(name='password', type=str, required=True, nullable=False)

change_password_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='old_password', type=str, required=True, nullable=False)
auth_parser.add_argument(name='new_password', type=str, required=True, nullable=False)

tokens_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='access_token', type=str, required=True)
auth_parser.add_argument(name='refresh_token', type=str, required=True)
