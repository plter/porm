# porm
Async Python ORM Framework

# Quick start

```python
async def entrypoint():
    ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
    ds.define_table("auth_user", Field("name"))

    @ds.with_connection
    async def task(c: DataSourceConnection):
        print(await c.select(c.auth_user.id > 0))

    await task()


asyncio.run(entrypoint())
```