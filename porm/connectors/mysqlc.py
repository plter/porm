"""
@author https://yunp.top
"""
from __future__ import annotations

from aiomysql import Pool, Connection, DictCursor

from porm.connectors.base_connector import BaseConnector
import aiomysql


class MySQLConnector(BaseConnector):

    def __init__(self, host: str, port: int, db: str, user: str, pwd: str, min_connections=0, max_connections=10):
        super().__init__(host, port, db, user, pwd, min_connections, max_connections)
        self._pool: Pool | None = None

    async def execute(self, callback):
        if not self._pool:
            self._pool = await aiomysql.create_pool(
                minsize=self.min_connections, maxsize=self.max_connections,
                host=self.host, port=self.port, db=self.db, user=self.user, password=self.pwd,
                autocommit=True
            )
        async with self._pool.acquire() as conn:  # type: Connection
            await conn.autocommit(True)
            async with conn.cursor(DictCursor) as cursor:  # type: DictCursor
                print(cursor)
            pass
