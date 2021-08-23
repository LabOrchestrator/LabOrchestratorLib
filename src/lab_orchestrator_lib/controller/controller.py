from typing import List

from lab_orchestrator_lib_auth.auth import generate_auth_token, LabInstanceTokenParams
from lab_orchestrator_lib.controller.adapter_controller import AdapterController
from lab_orchestrator_lib.controller.kubernetes_controller import NamespacedController, NotNamespacedController
from lab_orchestrator_lib.database.adapter import DockerImageAdapterInterface, LabAdapterInterface, \
    LabInstanceAdapterInterface, UserAdapterInterface
from lab_orchestrator_lib.kubernetes.api import NotNamespacedApi, NamespacedApi, APIRegistry
from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance, Identifier, User, LabInstanceKubernetes


class UserController:
    def __init__(self, adapter: UserAdapterInterface):
        self.adapter = adapter

    def get_all(self) -> List[User]:
        return self.adapter.get_all()

    def get(self, identifier) -> User:
        return self.adapter.get(identifier)


class NamespaceController(NotNamespacedController):
    template_file = "namespace_template.yaml"

    def _api(self) -> NotNamespacedApi:
        return self.registry.namespace

    def create(self, namespace):
        template_data = {'namespace': namespace}
        data = self._get_template(template_data)
        return self._api().create(data)


class NetworkPolicyController(NamespacedController):
    template_file = 'network_policy_template.yaml'

    def _api(self) -> NamespacedApi:
        return self.registry.network_policy

    def __init__(self, registry: APIRegistry):
        super().__init__(registry)
        self.default_name = "allow-same-namespace"

    def create(self, namespace):
        template_data = {'namespace': namespace, 'network_policy_name': self.default_name}
        data = self._get_template(template_data)
        return self._api().create(namespace, data)


class DockerImageController(AdapterController):
    def __init__(self, adapter: DockerImageAdapterInterface):
        super().__init__(adapter)

    def create(self, name, description, url) -> DockerImage:
        return self.adapter.create(name, description, url)


class VirtualMachineInstanceController(NamespacedController):
    template_file = 'vmi_template.yaml'

    def __init__(self, registry: APIRegistry, namespace_ctrl: NamespaceController,
                 docker_image_ctrl: DockerImageController):
        super().__init__(registry)
        self.namespace_ctrl = namespace_ctrl
        self.docker_image_ctrl = docker_image_ctrl

    def _api(self) -> NamespacedApi:
        return self.registry.virtual_machine_instance

    def create(self, namespace, lab: Lab):
        docker_image = self.docker_image_ctrl.get(lab.docker_image_id)
        template_data = {"cores": 3, "memory": "3G",
                         "vm_image": docker_image.url, "vmi_name": lab.docker_image_name,
                         "namespace": namespace}
        data = self._get_template(template_data)
        return self._api().create(namespace, data)

    def get_list_of_lab_instance(self, lab_instance: LabInstance, lab_instance_ctrl: 'LabInstanceController'):
        namespace_name = LabInstanceController.get_namespace_name(lab_instance, lab_instance_ctrl)
        namespace = self.namespace_ctrl.get(namespace_name)
        return self.get_list(namespace_name)

    def get_of_lab_instance(self, lab_instance: LabInstance, virtual_machine_instance_id,
                            lab_instance_ctrl: 'LabInstanceController'):
        namespace_name = LabInstanceController.get_namespace_name(lab_instance, lab_instance_ctrl)
        namespace = self.namespace_ctrl.get(namespace_name)
        return self.get(namespace_name, virtual_machine_instance_id)


class LabController(AdapterController):
    def __init__(self, adapter: LabAdapterInterface):
        super().__init__(adapter)

    def create(self, name: str, namespace_prefix: str, description: str, docker_image_id: Identifier,
               docker_image_name: str) -> Lab:
        return self.adapter.create(name=name, namespace_prefix=namespace_prefix, description=description,
                                   docker_image_id=docker_image_id, docker_image_name=docker_image_name)


class LabInstanceController(AdapterController):
    def __init__(self,
                 adapter: LabInstanceAdapterInterface,
                 virtual_machine_instance_ctrl: VirtualMachineInstanceController,
                 namespace_ctrl: NamespaceController,
                 lab_ctrl: LabController,
                 network_policy_ctrl: NetworkPolicyController,
                 user_ctrl: UserController,
                 secret_key: str):
        super().__init__(adapter)
        self.virtual_machine_instance_ctrl = virtual_machine_instance_ctrl
        self.namespace_ctrl = namespace_ctrl
        self.lab_ctrl = lab_ctrl
        self.network_policy_ctrl = network_policy_ctrl
        self.user_ctrl = user_ctrl
        self.secret_key = secret_key

    @staticmethod
    def get_namespace_name(lab_instance: LabInstance, lab_instance_ctrl):
        lab = lab_instance_ctrl.get(lab_instance.lab_id)
        return LabInstanceController.gen_namespace_name(lab, lab_instance.user_id, lab_instance.primary_key)

    @staticmethod
    def gen_namespace_name(lab: Lab, user_id, lab_instance_id):
        return f"{lab.namespace_prefix}-{user_id}-{lab_instance_id}"

    def create(self, lab_id: Identifier, user_id: Identifier) -> LabInstanceKubernetes:
        lab = self.lab_ctrl.get(lab_id)
        if lab is None:
            # TODO sinnvolle exception werfen
            raise Exception
        user = self.user_ctrl.get(user_id)
        if user is None:
            # TODO sinnvolle exception werfen
            raise Exception
        lab_instance = self.adapter.create(lab_id=lab_id, user_id=user_id)
        # create namespace
        namespace_name = LabInstanceController.gen_namespace_name(lab, user_id, lab_instance.primary_key)
        namespace = self.namespace_ctrl.create(namespace_name)
        # TODO fix response code
        # TODO log if deletion doesn't work
        #if namespace.response_code != 0:
        #    self.adapter.delete(lab_instance.primary_key)
        #    raise Exception
        # create network policy
        network_policy = self.network_policy_ctrl.create(namespace_name)
        #if network_policy.response_code != 0:
        #    self.adapter.delete(lab_instance.primary_key)
        #    self.namespace_ctrl.delete(namespace_name)
        #    raise Exception
        # create vmi
        vmi = self.virtual_machine_instance_ctrl.create(namespace_name, lab)
        #if vmi.response_code != 0:
        #    self.adapter.delete(lab_instance.primary_key)
        #    self.namespace_ctrl.delete(namespace_name)
        #    raise Exception
        lab_instance_token_params = LabInstanceTokenParams(lab_id, namespace_name, lab.docker_image_name)
        token = generate_auth_token(user_id=user_id, lab_instance_token_params=lab_instance_token_params,
                                    secret_key=self.secret_key)
        LabInstanceKubernetes(primary_key=lab_instance.primary_key, lab_id=lab_id, user_id=user_id, jwt_token=token)
        return lab_instance

    def delete(self, lab_instance: LabInstance):
        super().delete(lab_instance)
        lab = self.lab_ctrl.get(lab_instance.lab_id)
        namespace_name = LabInstanceController.gen_namespace_name(lab, lab_instance.user_id, lab_instance.primary_key)
        self.namespace_ctrl.delete(namespace_name)
        # this also deletes VMIs and all other resources in the namespace

    def get_list_of_user(self, user: User):
        # TODO list instead of item
        lab_instances = self.adapter.filter_by(user_id=user.primary_key)
        return lab_instances

    def save(self, obj: LabInstance) -> LabInstance:
        raise Exception("LabInstances can't be mutated.")
