import os


def _set_environ(env: str = 'DEV') -> str:
    # env can be DEV | PROD |TEST
    match env:
        case 'DEV':
            os.environ['FLASK_APP'] = 'app.py'
            os.environ['FLASK_ENV'] = 'development'
            os.environ['FLASK_DEBUG'] = '1'
            return f'Installed DEV environment'
        case 'PROD':
            os.environ['FLASK_APP'] = 'app.py'
            os.environ['FLASK_ENV'] = 'production'
            os.environ['FLASK_DEBUG'] = '0'
            return f'Installed PROD environment'
        case 'TEST':
            os.environ['FLASK_APP'] = 'test.py'
            os.environ['FLASK_ENV'] = 'testing'
            os.environ['FLASK_DEBUG'] = '1'
            return f'Installed TEST environment'
        case _:
            raise TypeError('env should be DEV|PROD|TEST')
