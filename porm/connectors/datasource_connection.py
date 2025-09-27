"""
@author https://yunp.top
"""
from pydal import DAL


class DataSourceConnection:

    def __init__(self, dal: DAL):
        super().__init__()
        self._dal = dal

    async def execute(self, query: str, args=None) -> int:
        raise NotImplementedError()

    async def fetchone(self) -> dict:
        raise NotImplementedError()

    async def fetchall(self) -> list[dict]:
        raise NotImplementedError()

    @property
    def lastrowid(self):
        raise NotImplementedError()

    def get_dal_field(self, name):
        return self._dal[name]

    def __getattr__(self, item):
        return self.get_dal_field(item)

    def __getitem__(self, item):
        return self.get_dal_field(item)

    async def select(self, query, *fields, **attributes) -> list[dict]:
        await self.execute(self._dal(query)._select(*fields, **attributes))
        return await self.fetchall()

    async def select_one(self, query, *fields) -> dict:
        await self.execute(self._dal(query)._select(*fields, limitby=(0, 1)))
        return await self.fetchone()

    async def count(self, query, distinct=None) -> int:
        await self.execute(self._dal(query)._count(distinct))
        result = await self.fetchone()
        for v in result.values():
            return v
        return 0

    async def exists(self, query, distinct=None) -> bool:
        return (await self.count(query, distinct)) > 0

    async def insert(self, table, **fields) -> int:
        """
        :param table:
        :param fields:
        :return: The last row id
        """
        await self.execute(table._insert(**fields))
        return self.lastrowid

    async def update(self, query, **update_fields):
        return await self.execute(self._dal(query)._update(**update_fields))

    async def upsert(self, table, data: dict, on_duplicate: dict):
        raise NotImplementedError()
