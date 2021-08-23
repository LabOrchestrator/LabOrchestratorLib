from lab_orchestrator_lib.kubernetes.api import APIRegistry, NamespacedApi, NotNamespacedApi
from lab_orchestrator_lib.template_engine import TemplateEngine


class KubernetesController:
    template_file = None

    def __init__(self, registry: APIRegistry):
        self.registry = registry

    def _get_template(self, template_data) -> str:
        return TemplateEngine().replace_template(template=self.template_file, data=template_data)


class NamespacedController(KubernetesController):
    def _api(self) -> NamespacedApi:
        raise NotImplementedError()

    def get_list(self, namespace) -> str:
        return self._api().get_list(namespace)

    def get(self, namespace, identifier) -> str:
        return self._api().get(namespace, identifier)

    def delete(self, namespace, identifier) -> str:
        return self._api().delete(namespace, identifier)


class NotNamespacedController(KubernetesController):
    def _api(self) -> NotNamespacedApi:
        raise NotImplementedError()

    def get_list(self):
        return self._api().get_list()

    def get(self, identifier):
        return self._api().get(identifier)

    def delete(self, identifier):
        return self._api().delete(identifier)