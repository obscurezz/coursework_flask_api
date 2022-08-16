from project.tools.security_tool import __generate_salt, __create_security_file

if __name__ == '__main__':
    __create_security_file(__generate_salt(4), hash_name='sha256', iterations=3)
