"""Contains methods that are used to configure the Kubernetes API."""

import os
from dataclasses import dataclass
from typing import Optional

from lab_orchestrator_lib.kubernetes.api import Proxy, APIRegistry


@dataclass
class KubernetesConfig:
    """Configuration object that is used to create a Proxy and APIRegistry object.

    :arg service_account_token: Token that is used to authenticate against the Kubernetes API. This is probably the
                                token from a service account.
    :arg cacert: Ca certificate file that is used to secure the connection.
    :arg protocol: Either "https" or "http".
    :arg service_host: Host address of the Kubernetes API.
    :arg service_port: Port of the Kubernetes API.
    :arg base_uri: The base url that is used to connect to the Kubernetes API. (Combination of protocol, service_host and service_port)
    """
    service_account_token: Optional[str]
    cacert: Optional[str]
    protocol: str
    service_host: str
    service_port: str
    base_uri: str


def get_kubernetes_config():
    """Use this if you run the lib inside of Kubernetes.

    :return: A Kubernetes config that reads the token and ca cert from Kubernetes standard directories and it
    creates the other variables from Kubernetes variables.
    """
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
        service_account_token = file.read()
    cacert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    protocol = "https"
    kubernetes_service_host = os.environ["KUBERNETES_SERVICE_HOST"]
    kubernetes_service_port = os.environ["KUBERNETES_SERVICE_PORT"]
    base_uri = f"{protocol}://{kubernetes_service_host}:{kubernetes_service_port}"
    kubernetes_config = KubernetesConfig(service_account_token, cacert, protocol, kubernetes_service_host,
                                         kubernetes_service_port, base_uri)
    return kubernetes_config


def get_development_config():
    """Use this if you run the lib inside of Kubernetes.

    Reads the environment variables `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT`.

    :return: A Kubernetes config that disables SSL and assumes you are running `kubectl proxy`.
    """
    service_account_token = None
    cacert = None
    protocol = "http"
    kubernetes_service_host = os.environ["KUBERNETES_SERVICE_HOST"]
    kubernetes_service_port = os.environ["KUBERNETES_SERVICE_PORT"]
    base_uri = f"{protocol}://{kubernetes_service_host}:{kubernetes_service_port}"
    kubernetes_config = KubernetesConfig(service_account_token, cacert, protocol, kubernetes_service_host,
                                         kubernetes_service_port, base_uri)
    return kubernetes_config


def get_registry(kubernetes_config: KubernetesConfig):
    """Creates a Proxy and APIRegistry from the given Kuberntes_config.

    :param kubernetes_config: The Kubernetes config that should be used to create the proxy and api registry.
    :return: A APIRegistry that can be injected into Kubernetes controllers.
    """
    proxy = Proxy(kubernetes_config.base_uri, kubernetes_config.service_account_token, kubernetes_config.cacert)
    return APIRegistry(proxy)
