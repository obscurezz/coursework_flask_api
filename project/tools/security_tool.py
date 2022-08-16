import json
import secrets

from project.config import BASE_DIR


def __generate_salt(length: int) -> str:
    return secrets.token_hex(length)


def __create_security_file(salt: str, hash_name: str = 'sha256', iterations: int = 3) -> None:
    sec_dict = json.dumps({
        "PWD_SALT": salt,
        "PWD_HASH_NAME": hash_name,
        "PWD_HASH_ITERATIONS": iterations
    },
        indent=4)

    with open(BASE_DIR.joinpath('security.json'), 'w', encoding='utf-8') as sec_file:
        sec_file.write(sec_dict)
