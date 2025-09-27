"""
@author https://yunp.top
"""

from pydal import DAL, Field

from porm.connectors.base_connector import BaseConnector
from porm.exceptions.porm_exception import PormException


class DataSource:

    def __init__(
            self, dialect: str, host: str, port: int, db: str, user: str, pwd: str,
            min_connections=0, max_connections=10
    ):
        super().__init__()

        self._dal = DAL(
            uri=f"{dialect}://root:password@127.0.0.1/db",
            migrate=False,
            migrate_enabled=False,
            bigint_id=True,
            pool_size=0
        )

        if dialect == "mysql":
            from porm.connectors.mysqlc import MySQLConnector
            self._connector = MySQLConnector(self._dal, host, port, db, user, pwd, min_connections, max_connections)
        elif dialect == "postgres":
            from porm.connectors.pgc import PgConnector
            self._connector = PgConnector(self._dal, host, port, db, user, pwd, min_connections, max_connections)
        else:
            raise PormException(f"Dialect {dialect} not supported")

    def define_table(self, tablename: str, *fields, **kwargs):
        self._dal.define_table(tablename, *fields, **kwargs)

    def with_connection(self, target):
        async def task(*args, **kwargs):
            async def callback(conn):
                return await target(conn, *args, **kwargs)

            return await self.execute(callback)

        return task

    def connector(self) -> BaseConnector:
        return self._connector

    async def execute(self, callback):
        return await self._connector.execute(callback)
