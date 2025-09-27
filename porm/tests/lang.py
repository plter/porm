import asyncio
from inspect import isawaitable
from unittest import TestCase


class LangTests(TestCase):
    def test_async_feature(self):
        async def hello():
            print("Hello World")

        r = hello()
        if isawaitable(r):
            asyncio.run(r)
        pass
