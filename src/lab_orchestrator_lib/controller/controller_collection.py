from dataclasses import dataclass

from lab_orchestrator_lib.controller.controller import NamespaceController, NetworkPolicyController, \
    DockerImageController, VirtualMachineInstanceController, LabController, LabInstanceController, UserController
from lab_orchestrator_lib.database.adapter import DockerImageAdapterInterface, LabInstanceAdapterInterface, \
    LabAdapterInterface, UserAdapterInterface
from lab_orchestrator_lib.kubernetes.api import APIRegistry


@dataclass
class ControllerCollection:
    user_ctrl: UserController
    namespace_ctrl: NamespaceController
    network_policy_ctrl: NetworkPolicyController
    docker_image_ctrl: DockerImageController
    virtual_machine_instance_ctrl: VirtualMachineInstanceController
    lab_ctrl: LabController
    lab_instance_ctrl: LabInstanceController


def create_controller_collection(
        registry: APIRegistry,
        user_adapter: UserAdapterInterface,
        docker_image_adapter: DockerImageAdapterInterface,
        lab_adapter: LabAdapterInterface,
        lab_instance_adapter: LabInstanceAdapterInterface,
        secret_key: str):
    user_ctrl = UserController(user_adapter)
    namespace_ctrl = NamespaceController(registry)
    network_policy_ctrl = NetworkPolicyController(registry)
    docker_image_ctrl = DockerImageController(docker_image_adapter)
    virtual_machine_instance_ctrl = VirtualMachineInstanceController(registry, namespace_ctrl, docker_image_ctrl)
    lab_ctrl = LabController(lab_adapter)
    lab_instance_ctrl = LabInstanceController(
        adapter=lab_instance_adapter,
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
        docker_image_ctrl=docker_image_ctrl,
        virtual_machine_instance_ctrl=virtual_machine_instance_ctrl,
        lab_ctrl=lab_ctrl,
        lab_instance_ctrl=lab_instance_ctrl,
    )
