"""Contains a collection of controllers and a method to create all controllers at once."""

from dataclasses import dataclass

from lab_orchestrator_lib.controller.controller import NamespaceController, NetworkPolicyController, \
    DockerImageController, VirtualMachineInstanceController, LabController, LabInstanceController, UserController, \
    LabDockerImageController
from lab_orchestrator_lib.database.adapter import DockerImageAdapterInterface, LabInstanceAdapterInterface, \
    LabAdapterInterface, UserAdapterInterface, LabDockerImageAdapterInterface
from lab_orchestrator_lib.kubernetes.api import APIRegistry


@dataclass
class ControllerCollection:
    """Contains all controllers."""
    user_ctrl: UserController
    namespace_ctrl: NamespaceController
    network_policy_ctrl: NetworkPolicyController
    docker_image_ctrl: DockerImageController
    lab_docker_image_ctrl: LabDockerImageController
    virtual_machine_instance_ctrl: VirtualMachineInstanceController
    lab_ctrl: LabController
    lab_instance_ctrl: LabInstanceController


def create_controller_collection(
        registry: APIRegistry,
        user_adapter: UserAdapterInterface,
        docker_image_adapter: DockerImageAdapterInterface,
        lab_docker_image_adapter: LabDockerImageAdapterInterface,
        lab_adapter: LabAdapterInterface,
        lab_instance_adapter: LabInstanceAdapterInterface,
        secret_key: str):
    """Initializes all controllers.

    :param registry: APIRegistry that should be injected into Kubernetes controllers.
    :param user_adapter: User adapter that should be injected into the controllers.
    :param docker_image_adapter: Docker image adapter that should be injected into the controllers.
    :param lab_docker_image_adapter: Lab docker image adapter that should be injected into the controllers.
    :param lab_adapter: Lab adapter that should be injected into the controllers.
    :param lab_instance_adapter: Lab instance adapter that should be injected into the controllers.
    :param secret_key: Secret key that should be used to create JWT tokens.
    :return: A controller collection with initialized controllers.
    """
    user_ctrl = UserController(user_adapter)
    namespace_ctrl = NamespaceController(registry)
    network_policy_ctrl = NetworkPolicyController(registry)
    docker_image_ctrl = DockerImageController(docker_image_adapter)
    lab_docker_image_ctrl = LabDockerImageController(lab_docker_image_adapter)
    virtual_machine_instance_ctrl = VirtualMachineInstanceController(
        registry=registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
        lab_docker_image_ctrl=lab_docker_image_ctrl
    )
    lab_ctrl = LabController(lab_adapter)
    lab_instance_ctrl = LabInstanceController(
        adapter=lab_instance_adapter,
        lab_docker_image_ctrl=lab_docker_image_ctrl,
        virtual_machine_instance_ctrl=virtual_machine_instance_ctrl,
        namespace_ctrl=namespace_ctrl,
        lab_ctrl=lab_ctrl,
        network_policy_ctrl=network_policy_ctrl,
        user_ctrl=user_ctrl,
        secret_key=secret_key,
    )
    return ControllerCollection(
        user_ctrl=user_ctrl,
        namespace_ctrl=namespace_ctrl,
        network_policy_ctrl=network_policy_ctrl,
        lab_docker_image_ctrl=lab_docker_image_ctrl,
        docker_image_ctrl=docker_image_ctrl,
        virtual_machine_instance_ctrl=virtual_machine_instance_ctrl,
        lab_ctrl=lab_ctrl,
        lab_instance_ctrl=lab_instance_ctrl,
    )
