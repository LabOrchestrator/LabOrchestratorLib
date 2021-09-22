"""Contains generic controllers that can be used for Kubernetes controllers."""
from typing import Optional

from lab_orchestrator_lib.kubernetes.api import APIRegistry, NamespacedApi, NotNamespacedApi
from lab_orchestrator_lib.template_engine import TemplateEngine


class KubernetesController:
    """Base class for Kubernetes controllers.

    All Kubernetes controllers should inherit from KubernetesController. This class adds a method to get templates that
    are used for the resources.

    :param template_file: This file is a class attribute and should be overwritten by the class. It should have the
                          filename of a template in `lab_orchestrator_lib/templates`.
    """

    template_file = None

    def __init__(self, registry: APIRegistry, template_engine: Optional[TemplateEngine] = None):
        """Initializes a KubernetesController.

        :param registry: The APIRegistry that should be used.
        :param template_engine: Optional template engine that is used to read the templates. If set to None the default
                                is `lab_orchestrator_lib.template_engine.TemplateEngine`.
        """
        self.registry = registry
        if template_engine is None:
            self.template_engine = TemplateEngine()
        else:
            self.template_engine = template_engine

    def _get_template(self, template_data) -> str:
        """Returns a template filled with the template data.

        :param template_data: Data that should be inserted into the template.
        :return: YAML str template with the data filled.
        """
        return self.template_engine.replace_template(template=self.template_file, data=template_data)


class NamespacedController(KubernetesController):
    """Abstract base controller for namespaced resources.

    All Kubernetes controllers that uses namespaced api resources should inherit from this class.
    """

    def _api(self) -> NamespacedApi:
        """Gives an instance of the namespaced api that is used in this controller.

        :return: An instance of the namespaced api.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_list(self, namespace) -> str:
        """Gives a list of all objects in the namespace.

        :param namespace: Namespace where to get the objects from.
        :return: A YAML string that contains all objects.
        """
        return self._api().get_list(namespace)

    def get(self, namespace, identifier) -> str:
        """Gives a specific object in the namespace.

        :param namespace: Namespace of the object.
        :param identifier: Identifier of the object.
        :return: A YAML string that contains the object.
        """
        return self._api().get(namespace, identifier)

    def delete(self, namespace, identifier) -> str:
        """Deletes a specific object in the namespace.

        :param namespace: Namespace of the object.
        :param identifier: Identifier of the object.
        :return: A string that contains the deletion status.
        """
        return self._api().delete(namespace, identifier)


class NotNamespacedController(KubernetesController):
    """Abstract base controller for not namespaced resources.

    All Kubernetes controllers that uses not namespaced api resources should inherit from this class.
    """

    def _api(self) -> NotNamespacedApi:
        """Gives an instance of the not namespaced api that is used in this controller.

        :return: An instance of the not namespaced api.
        :raise NotImplementedError: Method needs to be implemented.
        """
        raise NotImplementedError()

    def get_list(self):
        """Gives a list of all objects.

        :return: A YAML string that contains all objects.
        """
        return self._api().get_list()

    def get(self, identifier):
        """Gives a specific object.

        :param identifier: Identifier of the object.
        :return: A YAML string that contains the object.
        """
        return self._api().get(identifier)

    def delete(self, identifier):
        """Deletes a specific object.

        :param identifier: Identifier of the object.
        :return: A string that contains the deletion status.
        """
        return self._api().delete(identifier)
