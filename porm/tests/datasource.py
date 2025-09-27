import asyncio
import unittest

from porm import DataSource, Field
from porm.connectors.datasource_connection import DataSourceConnection


class DataSourceTests(unittest.TestCase):

    def test_create_datasource(self):
        ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
        print(ds)

    def test_connect_mysql(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table("auth_user", Field("name"))

            @ds.wrapper
            async def task(c: DataSourceConnection):
                # await conn.execute("select * from auth_user")
                # r = await conn.fetchall()
                # print(r)
                # print(await c.select_one(c.auth_user.id > 0))
                print(await c.count(c.auth_user.id > 0))

            await task()

        asyncio.run(entrypoint())

    def test_select(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table("auth_user", Field("name"))

            @ds.wrapper
            async def task(c: DataSourceConnection):
                print(await c.select(c.auth_user.id > 0))

            await task()

        asyncio.run(entrypoint())

    def test_count(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table("auth_user", Field("name"))

            @ds.wrapper
            async def task(c: DataSourceConnection):
                print(await c.count(c.auth_user.id > 0))

            await task()

        asyncio.run(entrypoint())

    def test_insert(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table("auth_user", Field("name"), Field("login"))

            @ds.wrapper
            async def task(c: DataSourceConnection):
                print(await c.insert(
                    c.auth_user, name="Zhang", login="tutu", on_duplicate_key_update=dict(name="Z")
                ))

            await task()

        asyncio.run(entrypoint())

    def test_update(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table("auth_user", Field("name"), Field("login"))

            @ds.wrapper
            async def task(c: DataSourceConnection):
                print(await c.update(c.auth_user.name == "Zhang", name="Zhang San"))

            await task()

        asyncio.run(entrypoint())

    def test_upsert(self):
        async def entrypoint():
            ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
            ds.define_table(
                "auth_user",
                Field("name"),
                Field("login"),
                Field("first_name"),
                Field("last_name"),
                Field("age")
            )

            @ds.wrapper
            async def task(c: DataSourceConnection):
                print(await c.upsert(
                    c.auth_user,
                    data=dict(name="Zhang", first_name="Donald-B", last_name="Trump"),
                    on_duplicate=dict(name="Li'1", age=10)
                ))

            await task()

        asyncio.run(entrypoint())
