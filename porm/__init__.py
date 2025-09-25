"""
@author https://yunp.top
"""
from pydal import DAL, Field

from porm.connectors.mysqlc import MySQLConnector
from porm.connectors.pgc import PgConnector
from porm.exceptions.porm_exception import PormException


class DataSource:

    def __init__(self, dialect: str, host: str, port: int, db: str, user: str, pwd: str):
        super().__init__()

        if dialect == "mysql":
            self._connector = MySQLConnector(host, port, db, user, pwd)
        elif dialect == "postgres":
            self._connector = PgConnector(host, port, db, user, pwd)
        else:
            raise PormException(f"Dialect {dialect} not supported")

        self._dal = DAL(
            uri=f"{dialect}://root:password@127.0.0.1/db",
            migrate=False,
            migrate_enabled=False,
            bigint_id=True,
            pool_size=0
        )

    def define_table(self, tablename: str, *fields, **kwargs):
        self._dal.define_table(tablename=tablename, *fields, **kwargs)
