"""
@author https://yunp.top
"""
from pydal import DAL


class BaseConnector:

    def __init__(
            self,
            dal: DAL,
            host: str, port: int, db: str, user: str, pwd: str,
            min_connections=0, max_connections=10
    ):
        super().__init__()
        self._dal = dal
        self._host = host
        self._port = port
        self._db = db
        self._user = user
        self._pwd = pwd
        self._min_connections = min_connections
        self._max_connections = max_connections

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
        return self._user

    @property
    def pwd(self):
        return self._pwd

    @property
    def min_connections(self):
        return self._min_connections

    @property
    def max_connections(self):
        return self._max_connections

    @property
    def dal(self):
        return self._dal

    async def execute(self, callback):
        raise NotImplementedError()

    async def pool(self):
        raise NotImplementedError
