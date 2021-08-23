import re
from typing import Any, Dict, Union, TextIO, Hashable

import yaml as yaml_library
import importlib.resources as pkg_resources
from . import templates


_path_matcher = re.compile(r'\$\{([^}^{]+)\}')

DataType = Dict[str, Any]
YamlStrType = Union[str, TextIO]
YamlType = Union[Dict[Hashable, Any], list, None]


def _path_constructor_factory(data: DataType, strict: bool):
    """Constructor factory for yaml.

    A factory that creates a constructor method, that replaces yaml-variables with the values in the data dictionary.

    :param data: dictionary that replaces yaml-variables.
    :param strict: if this is False all yaml variables that are not in the data dictionary will have a default value.
    :return: yaml constructor.
    """
    def path_constructor(loader, node):
        value = node.value
        match = _path_matcher.match(value)
        var = match.group()[2:-1]
        if strict:
            # raise exception if key is not found
            val = data[var]
        else:
            # default value if key is not found
            val = data.get(var)
        # needed to prevent converting integers to strings
        if value[match.end():] == "":
            return val
        else:
            return str(val) + value[match.end():]
    return path_constructor


class _VariableLoader(yaml_library.FullLoader):
    """Loader that is used for replacing yaml-variables."""
    yaml_constructors = yaml_library.FullLoader.yaml_constructors.copy()
    yaml_implicit_resolvers = yaml_library.FullLoader.yaml_implicit_resolvers.copy()


class TemplateEngine:
    """Yaml Template Engine.

    Used to replace yaml-variables.
    """

    def __init__(self, yaml_lib=yaml_library):
        self.yaml_lib = yaml_lib

    def load(self, yaml_str: YamlStrType, data: DataType, strict: bool = False) -> YamlType:
        """Parses a yaml string to a python object and replaces yaml-variables.

        :param yaml_str: The yaml string that should be parsed.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
            the default value None will be used.
        :return: yaml object.
        """
        _VariableLoader.add_implicit_resolver('!path', _path_matcher, None)
        _VariableLoader.add_constructor('!path', _path_constructor_factory(data, strict))
        p = self.yaml_lib.load(yaml_str, Loader=_VariableLoader)
        return p

    def load_template(self, template: str, data: DataType, strict: bool = False) -> YamlType:
        """Reads a template from the template module and parses the content as yaml to a python object and replaces
        yaml-variables.

        :param template: The template that contains the yaml.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
        the default value None will be used.
        :return: yaml object.
        """
        cont = pkg_resources.read_text(templates, template)
        return self.load(cont, data, strict)

    def load_file(self, filename: str, data: DataType, strict: bool = False) -> YamlType:
        """Reads a file and parses the content as yaml to a python object and replaces yaml-variables.

        :param filename: The file that contains the yaml.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
        the default value None will be used.
        :return: yaml object.
        """
        with open(filename) as cont:
            return self.load(cont, data, strict)

    def dump(self, yaml: Union[YamlType, Any]) -> str:
        """Converts a yaml object back to a string."""
        return self.yaml_lib.dump(yaml, Dumper=self.yaml_lib.Dumper, allow_unicode=True)

    def replace_template(self, template: str, data: DataType, strict: bool = False) -> str:
        """Reads a template and replaces the variables.

        :param template: The template that contains the yaml.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
        the default value None will be used.
        :return: The file content as string with replaced variables.
        """
        yaml = self.load_template(template, data, strict)
        return self.dump(yaml)

    def replace_file(self, filename: str, data: DataType, strict: bool = False) -> str:
        """Reads a file and replaces the variables.

        :param filename: The file that contains the yaml.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
        the default value None will be used.
        :return: The file content as string with replaced variables.
        """
        yaml = self.load_file(filename, data, strict)
        return self.dump(yaml)

    def replace(self, yaml_str: YamlStrType, data: DataType) -> str:
        """Replaces the variables in the yaml string.

        :param yaml_str: The yaml string that should be replaced.
        :param data: The data that should be inserted into the yaml-variables.
        :param strict: If True, an error will be thrown when variables have no value in the data dictionary. If false
        the default value None will be used.
        :return: The yaml string with replaced variables.
        """
        yaml = self.load(yaml_str, data)
        return self.dump(yaml)
