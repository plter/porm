"""
@author https://yunp.top
"""
from __future__ import annotations

from aiomysql import Pool, Connection, DictCursor
from pydal import DAL
from pymysql import IntegrityError

from porm.connectors.base_connector import BaseConnector
import aiomysql

from porm.connectors.datasource_connection import DataSourceConnection


class MySQLConnection(DataSourceConnection):

    def __init__(self, dal: DAL, cursor: DictCursor):
        super().__init__(dal)
        self._cursor: DictCursor = cursor

    async def execute(self, query: str, args=None) -> int:
        return await self._cursor.execute(query, args)

    async def fetchone(self) -> dict:
        return await self._cursor.fetchone()

    async def fetchall(self) -> list[dict]:
        return await self._cursor.fetchall()

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    async def upsert(self, table, data: dict, on_duplicate: dict):
        query: str = (table._insert(**data)).strip()
        if query[-1] == ";":
            query = query[:-1]
        update = ", ".join(
            map(
                lambda item: item[0] + "='" + str(item[1]).replace("'", "\\'") + "'",
                on_duplicate.items()
            )
        )
        query = f"{query} ON DUPLICATE KEY UPDATE {update};"
        print(query)
        await self.execute(query)
        return self.lastrowid


class MySQLConnector(BaseConnector):

    def __init__(
            self, dal: DAL, host: str, port: int, db: str, user: str, pwd: str,
            min_connections=0,
            max_connections=10
    ):
        super().__init__(dal, host, port, db, user, pwd, min_connections, max_connections)
        self._pool: Pool | None = None

    async def pool(self):
        if not self._pool:
            self._pool = await aiomysql.create_pool(
                minsize=self.min_connections, maxsize=self.max_connections,
                host=self.host, port=self.port, db=self.db, user=self.user, password=self.pwd,
                autocommit=True
            )
        return self._pool

    async def execute(self, callback):
        pool = await self.pool()
        async with pool.acquire() as conn:  # type: Connection
            await conn.autocommit(True)
            async with conn.cursor(DictCursor) as cursor:  # type: DictCursor
                return await callback(MySQLConnection(self.dal, cursor))
