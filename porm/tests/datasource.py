import unittest

from porm import DataSource


class DataSourceTests(unittest.TestCase):

    def test_create_datasource(self):
        ds = DataSource(dialect="mysql", host="127.0.0.1", port=5036, db="porm", user="root", pwd="wM1LKvy8")
        print(ds)
