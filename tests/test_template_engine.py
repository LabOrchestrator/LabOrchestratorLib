import unittest
import pathlib
import yaml as yaml_lib

from lab_orchestrator_lib.template_engine import TemplateEngine

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()


class TemplateEngineTestCase(unittest.TestCase):
    def test_load(self):
        yaml = TemplateEngine().load("hallo:\n  - eins\n  - zwei", {})
        self.assertEqual(yaml, {"hallo": ["eins", "zwei"]})

    def test_load_var(self):
        yaml = TemplateEngine().load("hallo:\n  - eins\n  - zwei\n  - ${drei}", {"drei": "fünf"})
        self.assertDictEqual(yaml, {"hallo": ["eins", "zwei", "fünf"]})

    def test_load_doesnt_change_yaml_constructors(self):
        yaml_str = "hallo:\n  - eins\n  - zwei\n  - ${drei}"
        yaml = TemplateEngine().load(yaml_str, {"drei": "fünf"})
        self.assertDictEqual(yaml, {"hallo": ["eins", "zwei", "fünf"]})
        yaml_without_var = yaml_lib.load(yaml_str, Loader=yaml_lib.FullLoader)
        self.assertDictEqual(yaml_without_var, {"hallo": ["eins", "zwei", "${drei}"]})

    def test_load_var_types(self):
        yaml = TemplateEngine().load("hallo:\n  - 1\n  - 5.8\n  - ${drei}\n  - ${vier}", {"drei": True, "vier": 8})
        self.assertDictEqual(yaml, {"hallo": [1, 5.8, True, 8]})

    def test_load_file(self):
        yaml = TemplateEngine().load_file(f"{CURRENT_DIR}/resources/namespace_template.yaml", {"namespace": "lab-1"})
        expected = {"kind": "Namespace", "apiVersion": "v1", "metadata": {"name": "lab-1"}}
        self.assertDictEqual(yaml, expected)

    def test_load_file_defaults(self):
        yaml = TemplateEngine().load_file(f"{CURRENT_DIR}/resources/namespace_template.yaml", {})
        expected = {"kind": "Namespace", "apiVersion": "v1", "metadata": {"name": None}}
        self.assertDictEqual(yaml, expected)

    def test_load_file_strict(self):
        with self.assertRaises(KeyError):
            TemplateEngine().load_file(f"{CURRENT_DIR}/resources/namespace_template.yaml", {}, True)

    def test_replace(self):
        yaml = TemplateEngine().replace("hallo:\n  - eins\n  - zwei\n  - ${drei}", {"drei": "fünf"})
        self.assertEqual(yaml, "hallo:\n- eins\n- zwei\n- fünf\n")

    def test_replace_file(self):
        yaml = TemplateEngine().replace_file(f"{CURRENT_DIR}/resources/namespace_template.yaml", {"namespace": "lab-1"})
        expected = "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: lab-1\n"
        self.assertEqual(yaml, expected)


if __name__ == '__main__':
    unittest.main()
