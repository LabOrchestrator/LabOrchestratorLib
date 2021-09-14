import unittest

from lab_orchestrator_lib.controller.kubernetes_controller import KubernetesController, NamespacedController, \
    NotNamespacedController

from lab_orchestrator_lib.kubernetes.api import NamespacedApi, NotNamespacedApi
from tests.controller.mockup import get_mocked_registry


class KubernetesControllerTestCase(unittest.TestCase):
    def test_init(self):
        _, registry = get_mocked_registry(self)
        kubernetes_ctrl = KubernetesController(registry)
        self.assertEqual(kubernetes_ctrl.registry, registry)

    def test_get_template(self):
        _, registry = get_mocked_registry(self)
        kubernetes_ctrl = KubernetesController(registry)
        kubernetes_ctrl.template_file = "namespace_template.yaml"
        template = kubernetes_ctrl._get_template({"namespace": "lab-1"})
        expected = "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: lab-1\n"
        self.assertEqual(template, expected)


class NamespacedControllerTestCase(unittest.TestCase):
    def test_get_api(self):
        proxy, registry = get_mocked_registry(self)
        class ExampleApi(NamespacedApi):
            pass
        class ExampleCtrl(NamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        api = ctrl._api()
        self.assertIsInstance(api, ExampleApi)

    def test_get_list(self):
        this = self
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        expected_namespace = "ns1"
        class ExampleApi(NamespacedApi):
            def get_list(self, namespace: str) -> str:
                this.assertEqual(namespace, expected_namespace)
                return expected
        class ExampleCtrl(NamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.get_list(expected_namespace)
        self.assertEqual(ret, expected)

    def test_get(self):
        this = self
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        expected_namespace = "ns1"
        expected_id = "8"
        class ExampleApi(NamespacedApi):
            def get(self, namespace: str, identifier: str) -> str:
                this.assertEqual(namespace, expected_namespace)
                this.assertEqual(identifier, expected_id)
                return expected
        class ExampleCtrl(NamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.get(expected_namespace, expected_id)
        self.assertEqual(ret, expected)

    def test_delete(self):
        this = self
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        expected_namespace = "ns1"
        expected_id = "8"
        class ExampleApi(NamespacedApi):
            def delete(self, namespace: str, identifier: str) -> str:
                this.assertEqual(namespace, expected_namespace)
                this.assertEqual(identifier, expected_id)
                return expected
        class ExampleCtrl(NamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.delete(expected_namespace, expected_id)
        self.assertEqual(ret, expected)


class NotNamespacedControllerTestCase(unittest.TestCase):
    def test_get_api(self):
        proxy, registry = get_mocked_registry(self)
        class ExampleApi(NotNamespacedApi):
            pass
        class ExampleCtrl(NotNamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        api = ctrl._api()
        self.assertIsInstance(api, ExampleApi)

    def test_get_list(self):
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        class ExampleApi(NotNamespacedApi):
            def get_list(self) -> str:
                return expected
        class ExampleCtrl(NotNamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.get_list()
        self.assertEqual(ret, expected)

    def test_get(self):
        this = self
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        expected_identifier = "8"
        class ExampleApi(NotNamespacedApi):
            def get(self, identifier: str) -> str:
                this.assertEqual(identifier, expected_identifier)
                return expected
        class ExampleCtrl(NotNamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.get(expected_identifier)
        self.assertEqual(ret, expected)

    def test_delete(self):
        this = self
        proxy, registry = get_mocked_registry(self)
        expected = "hallo"
        expected_identifier = "8"
        class ExampleApi(NotNamespacedApi):
            def delete(self, identifier: str) -> str:
                this.assertEqual(identifier, expected_identifier)
                return expected
        class ExampleCtrl(NotNamespacedController):
            def _api(self):
                return ExampleApi(proxy)
        ctrl = ExampleCtrl(registry)
        ret = ctrl.delete(expected_identifier)
        self.assertEqual(ret, expected)

