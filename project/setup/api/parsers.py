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
change_password_parser.add_argument(name='old_password', type=str, required=True, nullable=False)
change_password_parser.add_argument(name='new_password', type=str, required=True, nullable=False)

tokens_parser: RequestParser = RequestParser()
tokens_parser.add_argument(name='access_token', type=str, required=True)
tokens_parser.add_argument(name='refresh_token', type=str, required=True)

new_user_parser: RequestParser = auth_parser.copy()
new_user_parser.add_argument(name='first_name', type=str, required=True, nullable=False)
new_user_parser.add_argument(name='last_name', type=str, required=True, nullable=False)

update_user_parser: RequestParser = RequestParser()
update_user_parser.add_argument(name='first_name', type=str, required=True, nullable=False)
update_user_parser.add_argument(name='last_name', type=str, required=True, nullable=False)
update_user_parser.add_argument(name='favorite_genre', type=int, required=False, nullable=True)
