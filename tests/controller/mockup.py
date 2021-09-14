import unittest
from typing import Tuple

from lab_orchestrator_lib.kubernetes.api import APIRegistry
from tests.kubernetes.mockups import ProxyMock


def get_mocked_registry(test_case: unittest.TestCase) -> Tuple[ProxyMock, APIRegistry]:
    proxy = ProxyMock("/api")
    proxy.test = test_case
    registry = APIRegistry(proxy)
    return proxy, registry