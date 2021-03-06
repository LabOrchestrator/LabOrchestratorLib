import unittest
from typing import Tuple

from lab_orchestrator_lib.kubernetes.api import APIRegistry, _API_EXTENSIONS_NOT_NAMESPACED, _API_EXTENSIONS_NAMESPACED
from tests.kubernetes.mockups import ProxyMock


def get_mocked_registry(test_case: unittest.TestCase) -> Tuple[ProxyMock, APIRegistry]:
    proxy = ProxyMock("/api")
    proxy.test = test_case
    registry = APIRegistry(proxy)
    return proxy, registry


def clear_registry():
    _API_EXTENSIONS_NAMESPACED = {}
    _API_EXTENSIONS_NOT_NAMESPACED = {}
