"""Contains all implementations of controllers.

In the documentation of this module "you" refers to the developer that uses this library, "your program" means the part
of software that uses the lab orchestrator lib and "our library" refers to the lab orchestrator lib.

When you use this library there are some controllers that you need to use to create resources and some that you don't
need to use. The documentation of the controllers gives you specific information about this.
"""

from typing import List, Optional

from lab_orchestrator_lib.template_engine import TemplateEngine
from lab_orchestrator_lib_auth.auth import generate_auth_token, LabInstanceTokenParams
from lab_orchestrator_lib.controller.adapter_controller import AdapterController
from lab_orchestrator_lib.controller.kubernetes_controller import NamespacedController, NotNamespacedController
from lab_orchestrator_lib.database.adapter import DockerImageAdapterInterface, LabAdapterInterface, \
    LabInstanceAdapterInterface, UserAdapterInterface, LabDockerImageAdapterInterface
from lab_orchestrator_lib.kubernetes.api import NotNamespacedApi, NamespacedApi, APIRegistry
from lab_orchestrator_lib.model.model import DockerImage, Lab, LabInstance, Identifier, User, LabInstanceKubernetes, \
    LabDockerImage


class UserController:
    """User controller.

    This is the only controller that has no create, delete or save methods because the lab orchestrator lib doesn't create users. It's
    part of the program that uses this library to manage the users. That means you can create, update and delete users
    by your own without using this controller.
    """

    def __init__(self, adapter: UserAdapterInterface):
        """Initializes a user controller.

        :param adapter: User adapter that should be used.
        """
        self.adapter = adapter

    def get_all(self) -> List[User]:
        """Gives all objects of the adapter.

        :return: A list of all objects of the adapter.
        """
        return self.adapter.get_all()

    def get(self, identifier: Identifier) -> User:
        """Gives a specific object of the adapter.

        :param identifier: The identifier of the object.
        :return: The specific object.
        """
        return self.adapter.get(identifier)


class NamespaceController(NotNamespacedController):
    """Controller of Kubernetes Namespaces.

    When you need to create, delete or get namespaces in your program you need to use this controller. Usually you don't
    need to create, get or delete namespaces by your own.
    """

    template_file = "namespace_template.yaml"

    def _api(self) -> NotNamespacedApi:
        """Gives an instance of the namespace api.

        :return: An instance of the namespace api.
        """
        return self.registry.namespace

    def create(self, namespace):
        """Creates a new namespace.

        :param namespace: The name of the namespace.
        :return: YAML str of the namespace.
        """
        template_data = {'namespace': namespace}
        data = self._get_template(template_data)
        return self._api().create(data)


class NetworkPolicyController(NamespacedController):
    """Controller of Kubernetes Namespaces.

    When you need to create, delete or get network policies in your program you need to use this controller. Usually you
    don't need to create, get or delete network policies by you own.
    """

    template_file = 'network_policy_template.yaml'

    def _api(self) -> NamespacedApi:
        """Gives an instance of the network policy api.

        :return: An instance of the network policy api.
        """
        return self.registry.network_policy

    def __init__(self, registry: APIRegistry, template_engine: Optional[TemplateEngine] = None):
        """Initializes a network policy controller.

        :param registry: The APIRegistry that should be used.
        :param template_engine: The template engine that should be used. If none: a default one is used.
        """
        super().__init__(registry, template_engine)
        self.default_name = "allow-same-namespace"

    def create(self, namespace):
        """Creates a new network policy.

        :param namespace: The name of the namespace where the network policy should be created.
        :return: YAML str of the network policy.
        """
        template_data = {'namespace': namespace, 'network_policy_name': self.default_name}
        data = self._get_template(template_data)
        return self._api().create(namespace, data)


class DockerImageController(AdapterController):
    """Docker image controller.

    This controller is used by the library to get access to docker images. When you want to add new docker images, get
    or delete old ones you can do it directly without using this controller.
    """

    def __init__(self, adapter: DockerImageAdapterInterface):
        """Initializes a docker image controller.

        :param adapter: The docker image adapter that is used to connect to the database.
        """
        super().__init__(adapter)

    def create(self, name, description, url) -> DockerImage:
        """Creates a new docker image.

        :param name: Name of the docker image.
        :param description: Description of the docker image.
        :param url: Url of the docker image.
        :return: The created docker image.
        """
        return self.adapter.create(name, description, url)


class LabDockerImageController(AdapterController):
    """Lab docker image controller.

    This controller is used by the library to get access to lab docker images. When you want to add new lab docker
    images, get or delete old ones you can do it directly without using this controller.
    """

    def __init__(self, adapter: LabDockerImageAdapterInterface):
        """Initializes a lab docker image controller.

        :param adapter: The lab docker image adapter that is used to connect to the database.
        """
        super().__init__(adapter)

    def create(self, lab_id: Identifier, docker_image_id: Identifier, docker_image_name: str) -> LabDockerImage:
        """Creates a new lab docker image.

        :param lab_id: Id of the lab.
        :param docker_image_id: Id of the docker image.
        :param docker_image_name: Name of the VM.
        :return: The created lab docker image.
        """
        return self.adapter.create(lab_id, docker_image_id, docker_image_name)


class LabController(AdapterController):
    """Lab controller.

    This controller is used by the library to get access to labs. When you want to add new labs, get
    or delete old ones you can do it directly without using this controller.
    """

    def __init__(self, adapter: LabAdapterInterface):
        """Initializes a lab controller.

        :param adapter: The lab adapter that is used to connect to the database.
        """
        super().__init__(adapter)

    def create(self, name: str, namespace_prefix: str, description: str) -> Lab:
        """Creates a new lab.

        :param name: The name of the lab.
        :param namespace_prefix: The namespace prefix of the lab.
        :param description: The description of the lab
        :return: The created docker image.
        """
        return self.adapter.create(name=name, namespace_prefix=namespace_prefix, description=description)


class VirtualMachineInstanceController(NamespacedController):
    """Controller of KubeVirts VMIs.

    When you need to create, delete or get VMIs in your program you need to use this controller. Usually you don't need
    to create or delete VMIs by your own. Starting a VMIs is done automatically when you create a lab instance.
    """

    template_file = 'vmi_template.yaml'

    def __init__(self, registry: APIRegistry, namespace_ctrl: NamespaceController,
                 docker_image_ctrl: DockerImageController, lab_docker_image_ctrl: LabDockerImageController,
                 template_engine: Optional[TemplateEngine] = None):
        """Initializes a virtual machine instance controller.

        :param registry: APIRegistry that should be used.
        :param namespace_ctrl: Namespace controller that should be used.
        :param docker_image_ctrl: Docker image controller that should be used.
        :param lab_docker_image_ctrl: Lab docker image controller that should be used.
        :param template_engine: The template engine that should be used. If none: a default one is used.
        """
        super().__init__(registry, template_engine)
        self.namespace_ctrl = namespace_ctrl
        self.docker_image_ctrl = docker_image_ctrl
        self.lab_docker_image_ctrl = lab_docker_image_ctrl

    def _api(self) -> NamespacedApi:
        """Gives an instance of the vmi api.

        :return: An instance of the vmi api.
        """
        return self.registry.virtual_machine_instance

    def create(self, namespace, lab_docker_image: LabDockerImage):
        """Creates a new virtual machine instance.

        :param namespace: Namespace of the virtual machine instance.
        :param lab_docker_image: Lab docker image that should be started.
        :return: YAML str of the created virtual machine instance.
        """
        docker_image = self.docker_image_ctrl.get(lab_docker_image.docker_image_id)
        template_data = {"cores": 3, "memory": "3G",
                         "vm_image": docker_image.url, "vmi_name": lab_docker_image.docker_image_name,
                         "namespace": namespace}
        data = self._get_template(template_data)
        return self._api().create(namespace, data)

    def get_list_of_lab_instance(self, lab_instance: LabInstance, lab_ctrl: LabController):
        """Gives a list of virtual machine instances that belongs to a specific lab instance.

        :param lab_instance: The lab instance.
        :param lab_ctrl: The lab controller that is used to get the namespace.
        :return: A list of VMIs that belong to this lab instance.
        """
        namespace_name = LabInstanceController.get_namespace_name(lab_instance, lab_ctrl)
        namespace = self.namespace_ctrl.get(namespace_name)
        return self.get_list(namespace_name)

    def get_of_lab_instance(self, lab_instance: LabInstance, virtual_machine_instance_id,
                            lab_ctrl: LabController):
        """Gives a specific of virtual machine instance that belongs to a specific lab instance.

        :param lab_instance: The lab instance.
        :param virtual_machine_instance_id: The id of the vmi.
        :param lab_ctrl: The lab controller that is used to get the namespace.
        :return: The specific VMI.
        """
        namespace_name = LabInstanceController.get_namespace_name(lab_instance, lab_ctrl)
        namespace = self.namespace_ctrl.get(namespace_name)
        return self.get(namespace_name, virtual_machine_instance_id)


class LabInstanceController(AdapterController):
    """Controller of lab instances.

    When you need to create, get or delete VMIs in your program you need to use this controller. Creating a new lab
    instance will automatically create a namespace, a network policy and start all VMIs of the referred lab. You should
    not delete a lab instance by your own, because then the namespace, network policy and the VMIs won't stop running
    in Kubernetes.
    """

    def __init__(self,
                 adapter: LabInstanceAdapterInterface,
                 virtual_machine_instance_ctrl: VirtualMachineInstanceController,
                 lab_docker_image_ctrl: LabDockerImageController,
                 namespace_ctrl: NamespaceController,
                 lab_ctrl: LabController,
                 network_policy_ctrl: NetworkPolicyController,
                 user_ctrl: UserController,
                 secret_key: str):
        """Initializes a lab instance controller.

        :param adapter: The lab instance adapter that is used to connect to the database.
        :param virtual_machine_instance_ctrl: The virtual machine instance controller that should be used.
        :param namespace_ctrl: The namespace controller that should be used.
        :param lab_ctrl: The lab controller that should be used.
        :param network_policy_ctrl: The network policy controller that should be used.
        :param user_ctrl: The user controller that should be used.
        :param secret_key: The secret key that should be used to create JWT tokens.
        """
        super().__init__(adapter)
        self.virtual_machine_instance_ctrl = virtual_machine_instance_ctrl
        self.lab_docker_image_ctrl = lab_docker_image_ctrl
        self.namespace_ctrl = namespace_ctrl
        self.lab_ctrl = lab_ctrl
        self.network_policy_ctrl = network_policy_ctrl
        self.user_ctrl = user_ctrl
        self.secret_key = secret_key

    @staticmethod
    def get_namespace_name(lab_instance: LabInstance, lab_ctrl: LabController) -> str:
        """Returns the namespace name where the resources of a lab instances are created.

        The namespace name is generated by a combination of the labs namespace prefix, the user id and the lab instance
        id. This namespace name is unique for every lab instance.

        :param lab_instance: The lab instance from which you want the namespace name.
        :param lab_ctrl: The lab controller that should be used.
        :return: The name of the namespace.
        """
        lab = lab_ctrl.get(lab_instance.lab_id)
        return LabInstanceController.gen_namespace_name(lab, lab_instance.user_id, lab_instance.primary_key)

    @staticmethod
    def gen_namespace_name(lab: Lab, user_id, lab_instance_id) -> str:
        """Generates the namespace name where the resources of a lab instances are created.

        The namespace name is generated by a combination of the labs namespace prefix, the user id and the lab instance
        id. This namespace name is unique for every lab instance.

        :param lab: The lab that is started.
        :param user_id: The user that starts this lab.
        :param lab_instance_id: The id of the lab instance.
        :return: The name of the namespace.
        """

        return f"{lab.namespace_prefix}-{user_id}-{lab_instance_id}"

    def create(self, lab_id: Identifier, user_id: Identifier) -> LabInstanceKubernetes:
        """Creates a lab instance.

        Creating a lab instance is equivalent to starting a lab for a user. This contains creating a namespace, a
        network policy in the namespace and one or more virtual machine instances. In addition to this a JWT token
        will be created with that the user is able to connect to the virtual machine instances through the LabVNC.

        :param lab_id: The id of the lab.
        :param user_id: The id of the user.
        :return: Returns a lab instance kubernetes object.
        :raise Exception: if parameters are invalid.
        """
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
        lab_docker_images = self.lab_docker_image_ctrl.get_by_attr('lab_id', lab_id)
        for lab_docker_image in lab_docker_images:
            print(f"Starting VMI: {lab_docker_image.docker_image_name} - {lab_docker_image.docker_image_id}")
            vmi = self.virtual_machine_instance_ctrl.create(namespace_name, lab_docker_image)
            #if vmi.response_code != 0:
            #    self.adapter.delete(lab_instance.primary_key)
            #    self.namespace_ctrl.delete(namespace_name)
            #    raise Exception
        allowed_vmis = [lab_docker_image.docker_image_name for lab_docker_image in lab_docker_images]
        lab_instance_token_params = LabInstanceTokenParams(lab_id, lab_instance.primary_key, namespace_name,
                                                           allowed_vmis)
        token = generate_auth_token(user_id=user_id, lab_instance_token_params=lab_instance_token_params,
                                    secret_key=self.secret_key)
        return LabInstanceKubernetes(primary_key=lab_instance.primary_key, lab_id=lab_id, user_id=user_id,
                                     jwt_token=token, allowed_vmis=allowed_vmis)

    def delete(self, lab_instance: LabInstance) -> None:
        """Deletes a lab instance.

        This also deletes the created namespace with all resources that are contained in this namespace.

        :param lab_instance: The lab instance that should be deleted.
        :return: None
        """
        lab = self.lab_ctrl.get(lab_instance.lab_id)
        namespace_name = LabInstanceController.gen_namespace_name(lab, lab_instance.user_id, lab_instance.primary_key)
        # this also deletes VMIs and all other resources in the namespace
        self.namespace_ctrl.delete(namespace_name)
        # now delete local object
        super().delete(lab_instance.primary_key)

    def get_list_of_user(self, user: User):
        """Gives a list of lab instances that belong to a specific user.

        :param user: The user that belongs to the lab instances.
        :return: A list of lab instances that belongs to the user.
        """
        # TODO list instead of item
        lab_instances = self.adapter.filter(user_id=user.primary_key)
        return lab_instances

    def save(self, obj: LabInstance) -> LabInstance:
        """Removes the inherited save method, because lab instances can't be changed.

        :raise Exception: Always.
        """
        raise Exception("LabInstances can't be mutated.")
