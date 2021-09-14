import unittest

from lab_orchestrator_lib.model.model import DockerImage

from lab_orchestrator_lib.controller.adapter_controller import AdapterController


class AdapterControllerTestCase(unittest.TestCase):
    def test_get_all(self):
        expected = "hallo"
        class Adapter:
            def get_all(self):
                return expected
        ctrl = AdapterController(Adapter())
        ret = ctrl.get_all()
        self.assertEqual(ret, expected)

    def test_get(self):
        this = self
        expected = "hallo"
        expected_id = "8"
        class Adapter:
            def get(self, identifier):
                this.assertEqual(expected_id, identifier)
                return expected
        ctrl = AdapterController(Adapter())
        ret = ctrl.get(expected_id)
        self.assertEqual(ret, expected)

    def test_get_by_attr(self):
        this = self
        expected = "hallo"
        expected_attr = "attr"
        expected_value = "value"
        class Adapter:
            def get_by_attr(self, attr, value):
                this.assertEqual(attr, expected_attr)
                this.assertEqual(value, expected_value)
                return expected
        ctrl = AdapterController(Adapter())
        ret = ctrl.get_by_attr(expected_attr, expected_value)
        self.assertEqual(ret, expected)

    def test_delete(self):
        this = self
        expected = "hallo"
        expected_identifier = "8"
        class Adapter:
            def delete(self, identifier):
                this.assertEqual(identifier, expected_identifier)
                return expected
        ctrl = AdapterController(Adapter())
        ret = ctrl.delete(expected_identifier)
        self.assertEqual(ret, expected)

    def test_save(self):
        this = self
        class ExampleObj(DockerImage):
            pass
        expected = ExampleObj("id", "name", "desc", "url")
        class Adapter:
            def save(self, obj):
                this.assertEqual(expected, obj)
                return obj
        ctrl = AdapterController(Adapter())
        ret = ctrl.save(expected)
        self.assertEqual(ret, expected)

    def test_filter(self):
        this = self
        expected = "hallo"
        expected_name = "power"
        class Adapter:
            def filter(self, **kwargs):
                this.assertDictEqual(kwargs, {'name': expected_name})
                return expected
        ctrl = AdapterController(Adapter())
        ret = ctrl.filter(name=expected_name)
        self.assertEqual(ret, expected)


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
