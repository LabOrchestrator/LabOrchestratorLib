import os
from dataclasses import dataclass
from typing import Optional

from lab_orchestrator_lib.kubernetes.api import Proxy, APIRegistry


@dataclass
class KubernetesConfig:
    service_account_token: Optional[str]
    cacert: Optional[str]
    protocol: str
    service_host: str
    service_port: str
    base_uri: str


def get_kubernetes_config():
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
    proxy = Proxy(kubernetes_config.base_uri, kubernetes_config.service_account_token, kubernetes_config.cacert)
    return APIRegistry(proxy)
