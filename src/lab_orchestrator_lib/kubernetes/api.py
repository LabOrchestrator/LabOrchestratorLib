"""Maps the Kubernetes API."""

import logging
from abc import ABC
from typing import Dict, Type, Callable, Union, Optional, Any

import requests

_API_EXTENSIONS_NAMESPACED: Dict[str, Type['NamespacedApi']] = {}
_API_EXTENSIONS_NOT_NAMESPACED: Dict[str, Type['NotNamespacedApi']] = {}


NamespacedApiDecorator = Callable[[Type['NamespacedApi'], ], Type['NamespacedApi']]
NotNamespacedApiDecorator = Callable[[Type['NotNamespacedApi'], ], Type['NotNamespacedApi']]


def add_api_namespaced(name: str) -> NamespacedApiDecorator:
    """Decorator that adds a namespaced api class to the APIRegistry.

    When adding your class to the APIRegistry you later are able to get an instance of the class through an attribute of
    an APIRegistry object.

    :param name: Name of the attribute in the APIRegistry where you should get the API.
    :return: Decorator that adds a namespaced api class to the APIRegistry.
    """

    def inner(cls: Type[NamespacedApi]) -> Type[NamespacedApi]:
        _API_EXTENSIONS_NAMESPACED[name] = cls
        return cls
    return inner


def add_api_not_namespaced(name: str) -> NotNamespacedApiDecorator:
    """Decorator that adds a not namespaced api class to the APIRegistry.

    When adding your class to the APIRegistry you later are able to get an instance of the class through an attribute of
    an APIRegistry object.

    :param name: Name of the attribute in the APIRegistry where you should get the API.
    :return: Decorator that adds a not namespaced api class to the APIRegistry.
    """
    def inner(cls: Type[NotNamespacedApi]) -> Type[NotNamespacedApi]:
        _API_EXTENSIONS_NOT_NAMESPACED[name] = cls
        return cls
    return inner


class Proxy:
    """This proxy is used to make requests to the Kubernetes API.

    This proxy adds authentication headers and checks the SSL certificates.
    """

    def __init__(self, base_uri: str, service_account_token: Optional[str] = None,
                 cacert: Optional[str] = None, insecure_ssl: bool = False, requests_lib=requests):
        """Initializes a proxy object.

        :param base_uri: The base uri that is added before every api address. (For example: "https://localhost:8000/")
        :param service_account_token: The token that is added into the bearer authorization header.
        :param cacert: The file path to the file containing the ca cert that should verify the ssl connection.
        :param insecure_ssl: If this is true, ssl will be deactivated.
        :param requests_lib: The requests library wich makes the requests. Default: requests, but can be changed for mockups.
        """
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
        """Makes a get request.

        This method makes a get request to the Kubernetes API with authorization added and the SSL certificates
        checked.

        :param address: API path without base_uri. The address is put together with the base_uri.
        :return: The text body of the response. Should be in the YAML format.
        """
        headers = {"Authorization": f"Bearer {self.service_account_token}"}
        response = self.requests.get(self.base_uri + address,
                                     headers=headers, verify=self.verify)
        return response.text

    def post(self, address: str, data: str) -> str:
        """Makes a post request.

        This method makes a post request to the Kubernetes API with authorization added and the SSL certificates
        checked.

        :param address: API path without base_uri. The address is put together with the base_uri.
        :param data: POST body data. Should be a YAML string.
        :return: The text body of the response. Should be in the YAML format.
        """
        headers = {"Authorization": f"Bearer {self.service_account_token}",
                   "Content-Type": "application/yaml"}
        response = self.requests.post(self.base_uri + address,
                                      data=data, headers=headers, verify=self.verify)
        return response.text

    def delete(self, address) -> str:
        """Makes a delete request.

        This method makes a delete request to the Kubernetes API with authorization added and the SSL certificates
        checked.

        :param address: API path without base_uri. The address is put together with the base_uri.
        :return: The text body of the response. Should be in the YAML format.
        """
        headers = {"Authorization": f"Bearer {self.service_account_token}"}
        response = self.requests.delete(self.base_uri + address,
                                        headers=headers, verify=self.verify)
        return response.text


class APIRegistry:
    """This class is a container of Kubernetes API endpoints.

    Kubernetes API endpoints could be registered in the APIRegistry with the decorators `add_api_namespaced`,
    `add_api_not_namespaced` with a given name. After registering them they are available through their given name
    as attribute of this class. For example you register the Blahaj-API as "blahaj" then you can access it like this:
    `APIRegistry(proxy).blahaj`. This gives us a convenient way to add and access the needed Kubernetes APIs.
    """

    def __init__(self, proxy: Proxy):
        """Initializes an APIRegistry object.

        :param proxy: The proxy that should be used to make requests. The proxy already contains all information about
                      the Kubernetes API addresses.
        """
        self.proxy = proxy

    def __dir__(self):
        """This method is used to make the dynamic attributes of this class available to autocompletion.

        :return: A list of attributes this object has.
        """
        keys = set(super().__dir__())
        keys = keys.union(_API_EXTENSIONS_NAMESPACED.keys())
        keys = keys.union(_API_EXTENSIONS_NOT_NAMESPACED.keys())
        return list(keys)

    def __getattr__(self, name) -> Union['NamespacedApi', 'NotNamespacedApi']:
        """Executed on every attribute name.

        This method gets called on every attribute that is called on an APIRegistry object. This is used to dynamically
        add the API classes as attributes.

        :param name: Name of the attribute that was looked for.
        :return: An instance of the API class that belongs to the given attribute name.
        :raise: AttributeError: If attribute is not found.
        """
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
        """Initializes an ApiExtension object.

        :param proxy: The proxy that should be used in this API to make requests.
        """
        self.proxy = proxy


class NamespacedApi(ApiExtension):
    """Abstract base class extension for resource object that are namespaced.

    :list_url: Will be formated with the variable "namespace".
    :detail_url: Will be formated with the variable "namespace" and "identifier".
    """

    def get_list(self, namespace: str) -> str:
        """Will get a list of all resource object in the namespace.

        :param namespace: The namespace where to get the list of resource object from.
        :return: A list of all resource object in the given namespace as YAML str.
        """
        return self.proxy.get(self.list_url.format(namespace=namespace))

    def create(self, namespace: str, data: str) -> str:
        """Creates a new resource object in the namespace.

        :param namespace: The namespace where the resource object should be created.
        :param data: The data of the resource object that is used to create it.
        :return: The newly added resource object as YAML string.
        """
        return self.proxy.post(self.list_url.format(namespace=namespace), data)

    def get(self, namespace: str, identifier: str) -> str:
        """Gets a specific resource object in the namespace.

        :param namespace: The namespace of the resource object.
        :param identifier: The identifier of the resource object.
        :return: The resource object as YAML str.
        """
        return self.proxy.get(self.detail_url.format(namespace=namespace, identifier=identifier))

    def delete(self, namespace: str, identifier: str) -> str:
        """Deletes a specific resource object in a namespace.

        :param namespace: The namespace of the resource object.
        :param identifier: The identifier of the resource object.
        :return: The deletion response.
        """
        return self.proxy.delete(self.detail_url.format(namespace=namespace, identifier=identifier))


class NotNamespacedApi(ApiExtension):
    """Abstract base class extension for resource object that are not namespaced.

    :list_url: Will not be formated and shouldn't contain variables.
    :detail_url: Will be formated with the variable "identifier".
    """

    def get_list(self) -> str:
        """Will get a list of all resource object.

        :return: A list of all resource object as YAML str.
        """
        return self.proxy.get(self.list_url)

    def create(self, data: str) -> str:
        """Creates a new resource object.

        :param data: The data of the resource object that is used to create it.
        :return: The newly added resource object as YAML string.
        """
        return self.proxy.post(self.list_url, data)

    def get(self, identifier: str) -> str:
        """Gets a specific resource object.

        :param identifier: The identifier of the resource object.
        :return: The resource object as YAML str.
        """
        return self.proxy.get(self.detail_url.format(identifier=identifier))

    def delete(self, identifier: str) -> str:
        """Deletes a specific resource object.

        :param identifier: The identifier of the resource object.
        :return: The deletion response.
        """
        return self.proxy.delete(self.detail_url.format(identifier=identifier))


@add_api_not_namespaced("namespace")
class Namespace(NotNamespacedApi):
    """Kubernetes Namespace API.

    The namespace api is used to create, get and delete namespaces in Kubernetes.
    """
    list_url = "/api/v1/namespaces"
    detail_url = "/api/v1/namespaces/{identifier}"


@add_api_namespaced("virtual_machine_instance")
class VirtualMachineInstance(NamespacedApi):
    """KubeVirt Virtual Machine Instance API.

    The virtual machine instance api is used to create, get and delete VMIs in Kubernetes. This only works when
    KubeVirt is installed in the Kubernetes cluster.
    """
    list_url = "/apis/kubevirt.io/v1alpha3/namespaces/{namespace}/virtualmachineinstances/"
    detail_url = "/apis/kubevirt.io/v1alpha3/namespaces/{namespace}/virtualmachineinstances/{identifier}"


@add_api_namespaced("network_policy")
class NetworkPolicy(NamespacedApi):
    """Kubernetes NetworkPolicy API.

    The network policy api is used to create, get and delete network policies in Kubernetes. This only works with a
    network plugin installed that implements network policies.
    """
    list_url = "/apis/networking.k8s.io/v1/namespaces/{namespace}/networkpolicies"
    detail_url = "/apis/networking.k8s.io/v1/namespaces/{namespace}/networkpolicies/{identifier}"
