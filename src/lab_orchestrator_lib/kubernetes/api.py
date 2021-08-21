import logging
from abc import ABC
from typing import Dict, Type, Callable, Union, Optional, Any

import requests

_API_EXTENSIONS_NAMESPACED: Dict[str, Type['NamespacedApi']] = {}
_API_EXTENSIONS_NOT_NAMESPACED: Dict[str, Type['NotNamespacedApi']] = {}


NamespacedApiDecorator = Callable[[Type['NamespacedApi'], ], Type['NamespacedApi']]
NotNamespacedApiDecorator = Callable[[Type['NotNamespacedApi'], ], Type['NotNamespacedApi']]


def add_api_namespaced(name: str) -> NamespacedApiDecorator:
    def inner(cls: Type[NamespacedApi]) -> Type[NamespacedApi]:
        _API_EXTENSIONS_NAMESPACED[name] = cls
        return cls
    return inner


def add_api_not_namespaced(name: str) -> NotNamespacedApiDecorator:
    def inner(cls: Type[NotNamespacedApi]) -> Type[NotNamespacedApi]:
        _API_EXTENSIONS_NOT_NAMESPACED[name] = cls
        return cls
    return inner


class Proxy:
    def __init__(self, base_uri: str, service_account_token: str = None,
                 cacert: str = None, insecure_ssl: str = False, requests_lib=requests):
        self.requests = requests_lib
        if service_account_token is None:
            logging.warning("No service account token.")
        if cacert is None:
            logging.warning("No cacert.")
        self.base_uri = base_uri
        self.service_account_token = service_account_token
        if insecure_ssl:
            self.verify = False
        elif cacert is None:
            self.verify = True
        else:
            self.verify = cacert

    def get(self, address: str) -> str:
        headers = {"Authorization": f"Bearer {self.service_account_token}"}
        response = self.requests.get(self.base_uri + address,
                                     headers=headers, verify=self.verify)
        return response.text

    def post(self, address: str, data: str) -> str:
        headers = {"Authorization": f"Bearer {self.service_account_token}",
                   "Content-Type": "application/yaml"}
        response = self.requests.post(self.base_uri + address,
                                      data=data, headers=headers, verify=self.verify)
        return response.text

    def delete(self, address) -> str:
        headers = {"Authorization": f"Bearer {self.service_account_token}"}
        response = self.requests.delete(self.base_uri + address,
                                        headers=headers, verify=self.verify)
        return response.text


class APIRegistry:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    def __dir__(self):
        keys = set(super().__dir__())
        keys = keys.union(_API_EXTENSIONS_NAMESPACED.keys())
        keys = keys.union(_API_EXTENSIONS_NOT_NAMESPACED.keys())
        return list(keys)

    def __getattr__(self, name) -> Union['NamespacedApi', 'NotNamespacedApi']:
        cls: Union[Optional[Type['NamespacedApi']], Optional[Type['NotNamespacedApi']]]
        if cls := _API_EXTENSIONS_NAMESPACED.get(name):
            return cls(self.proxy)
        if cls := _API_EXTENSIONS_NOT_NAMESPACED.get(name):
            return cls(self.proxy)
        raise AttributeError(f'{name} not found')


class ApiExtension(ABC):
    """Used to extend the APIRegistry.

    To extend the APIRegistry, you need to implement either the NamespacedApi or NotNamespacedApi. Then add one
    of the decorators add_api_namespaced or add_api_not_namespaced or use these methods to add the classes manually.
    After that you can access an instance of the extension through the proxy as attributes for example
    "proxy.namespace" or "proxy.virtual_machine_instance". With that instances you are able to access the Kubernetes
    Api with the methods in NamespacedApi and NotNamespacedApi for example get_list or create.

    :param list_url: Will be formatted. Which variables will be inserted depends on the ApiExtension type.
    :param details_url: Will be formatted. Which variables will be inserted depends on the ApiExtension type.
    """
    list_url = None
    detail_url = None

    def __init__(self, proxy: Proxy):
        self.proxy = proxy


class NamespacedApi(ApiExtension):
    """Abstract base class extension for resources that are namespaced.

    :list_url: Will be formated with the variable "namespace".
    :detail_url: Will be formated with the variable "namespace" and "identifier".
    """
    def get_list(self, namespace: str) -> str:
        return self.proxy.get(self.list_url.format(namespace=namespace))

    def create(self, namespace: str, data: str) -> str:
        return self.proxy.post(self.list_url.format(namespace=namespace), data)

    def get(self, namespace: str, identifier: str) -> str:
        return self.proxy.get(self.detail_url.format(namespace=namespace, identifier=identifier))

    def delete(self, namespace: str, identifier: str) -> str:
        return self.proxy.delete(self.detail_url.format(namespace=namespace, identifier=identifier))


class NotNamespacedApi(ApiExtension):
    """Abstract base class extension for resources that are not namespaced.

    :list_url: Will not be formated and shouldn't contain variables.
    :detail_url: Will be formated with the variable "identifier".
    """

    def get_list(self) -> str:
        return self.proxy.get(self.list_url)

    def create(self, data: str) -> str:
        return self.proxy.post(self.list_url, data)

    def get(self, identifier: str) -> str:
        return self.proxy.get(self.detail_url.format(identifier=identifier))

    def delete(self, identifier: str) -> str:
        return self.proxy.delete(self.detail_url.format(identifier=identifier))


@add_api_not_namespaced("namespace")
class Namespace(NotNamespacedApi):
    list_url = "/api/v1/namespaces"
    detail_url = "/api/v1/namespaces/{identifier}"


@add_api_namespaced("virtual_machine_instance")
class VirtualMachineInstance(NamespacedApi):
    list_url = "/apis/kubevirt.io/v1alpha3/namespaces/{namespace}/virtualmachineinstances/"
    detail_url = "/apis/kubevirt.io/v1alpha3/namespaces/{namespace}/virtualmachineinstances/{identifier}"


@add_api_namespaced("network_policy")
class NetworkPolicy(NamespacedApi):
    list_url = "/apis/networking.k8s.io/v1/namespaces/{namespace}/networkpolicies"
    detail_url = "/apis/networking.k8s.io/v1/namespaces/{namespace}/networkpolicies/{identifier}"
