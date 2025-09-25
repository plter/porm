"""
@author https://yunp.top
"""


class BaseConnector:

    def __init__(self, host: str, port: int, db: str, user: str, pwd: str):
        super().__init__()
        self._host = host
        self._port = port
        self._db = db
        self._user = user
        self._pwd = pwd

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def db(self):
        return self._db

    @property
    def user(self):
        return self._db

    @property
    def pwd(self):
        return self._pwd
