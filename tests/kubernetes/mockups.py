import unittest
from typing import Union

from lab_orchestrator_lib.kubernetes.api import Proxy


class NoneFailsafe:
    def __getattr__(self, item):
        def retno(*args, **kwargs):
            return None
        return retno


class ProxyMock(Proxy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_ret = None
        self.asserted_get_address = None
        self.post_ret = None
        self.asserted_post_address = None
        self.asserted_post_data = None
        self.delete_ret = None
        self.asserted_delete_address = None
        self.test: Union[unittest.TestCase, NoneFailsafe] = NoneFailsafe()

    def get(self, address: str) -> str:
        self.test.assertEqual(self.asserted_get_address, address)
        return self.get_ret

    def post(self, address: str, data: str) -> str:
        self.test.assertEqual(self.asserted_post_address, address)
        self.test.assertEqual(self.asserted_post_data, data)
        return self.post_ret

    def delete(self, address) -> str:
        self.test.assertEqual(self.asserted_delete_address, address)
        return self.delete_ret


class RequestsMock:
    pass


class RequestsResponseMock:
    def __init__(self, text):
        self.text = text