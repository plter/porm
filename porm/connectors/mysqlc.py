"""
@author https://yunp.top
"""
from porm.connectors.base_connector import BaseConnector


class MySQLConnector(BaseConnector):

    def __init__(self, host: str, port: int, db: str, user: str, pwd: str):
        super().__init__(host, port, db, user, pwd)
