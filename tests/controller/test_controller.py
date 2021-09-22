import unittest
from typing import Dict, Any

from lab_orchestrator_lib.template_engine import TemplateEngine, DataType

from lab_orchestrator_lib.kubernetes.api import Namespace, NetworkPolicy, VirtualMachineInstance

from lab_orchestrator_lib.model.model import User, DockerImage, Lab, Identifier, LabInstance, LabInstanceKubernetes, \
    LabDockerImage

from lab_orchestrator_lib.controller.controller import UserController, NamespaceController, NetworkPolicyController, \
    DockerImageController, VirtualMachineInstanceController, LabController, LabInstanceController, \
    LabDockerImageController

from lab_orchestrator_lib.database.adapter import UserAdapterInterface, DockerImageAdapterInterface, \
    LabAdapterInterface, LabInstanceAdapterInterface, LabDockerImageAdapterInterface
from tests.controller.mockup import get_mocked_registry


class UserControllerTestCase(unittest.TestCase):
    def test_init(self):
        class ExampleUserAdapterInterface(UserAdapterInterface):
            pass
        expected = ExampleUserAdapterInterface()
        ctrl = UserController(expected)
        self.assertEqual(ctrl.adapter, expected)

    def test_get_all(self):
        expected = [User(1), User(2)]
        class ExampleUserAdapterInterface(UserAdapterInterface):
            def get_all(self):
                return expected
        ctrl = UserController(ExampleUserAdapterInterface())
        ret = ctrl.get_all()
        self.assertListEqual(ret, expected)

    def test_get(self):
        this = self
        expected_id = 1
        expected = User(expected_id)
        class ExampleUserAdapterInterface(UserAdapterInterface):
            def get(self, identifier):
                this.assertEqual(identifier, expected_id)
                return expected
        ctrl = UserController(ExampleUserAdapterInterface())
        ret = ctrl.get(expected_id)
        self.assertEqual(ret, expected)


class NamespaceControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy, self.registry = get_mocked_registry(self)

    def test_api(self):
        ctrl = NamespaceController(self.registry)
        self.assertIsInstance(ctrl._api(), Namespace)

    def test_create(self):
        this = self
        expected = "success"
        expected_namespace = "ns1"
        expected_template_data = {"namespace": expected_namespace}
        expected_data = "bla"
        class ExampleTemplateEngine(TemplateEngine):
            def replace_template(self, template: str, data: DataType, strict: bool = False) -> str:
                this.assertEqual(data, expected_template_data)
                return expected_data
        class ExampleApi:
            def create(self, data: str) -> str:
                this.assertEqual(data, expected_data)
                return expected
        ctrl = NamespaceController(self.registry, template_engine=ExampleTemplateEngine())
        ctrl._api = lambda : ExampleApi()
        ret = ctrl.create(expected_namespace)
        self.assertEqual(ret, expected)


class NetworkPolicyControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy, self.registry = get_mocked_registry(self)

    def test_api(self):
        ctrl = NetworkPolicyController(self.registry)
        self.assertIsInstance(ctrl._api(), NetworkPolicy)

    def test_create(self):
        this = self
        expected = "success"
        expected_namespace = "ns1"
        expected_template_data = {"namespace": expected_namespace, "network_policy_name": "allow-same-namespace"}
        expected_data = "bla"
        class ExampleTemplateEngine(TemplateEngine):
            def replace_template(self, template: str, data: DataType, strict: bool = False) -> str:
                this.assertEqual(data, expected_template_data)
                return expected_data
        class ExampleApi:
            def create(self, namespace, data: str) -> str:
                this.assertEqual(namespace, expected_namespace)
                this.assertEqual(data, expected_data)
                return expected
        ctrl = NetworkPolicyController(self.registry, template_engine=ExampleTemplateEngine())
        ctrl._api = lambda : ExampleApi()
        ret = ctrl.create(expected_namespace)
        self.assertEqual(ret, expected)


class DockerImageControllerTestCase(unittest.TestCase):
    def test_init(self):
        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            pass
        expected = ExampleDockerImageAdapterInterface()
        ctrl = DockerImageController(expected)
        self.assertEqual(ctrl.adapter, expected)

    def test_create(self):
        this = self
        expected = DockerImage("8", "name", "desc", "url")
        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            def create(self, name: str, description: str, url: str) -> DockerImage:
                this.assertEqual(name, expected.name)
                this.assertEqual(description, expected.description)
                this.assertEqual(url, expected.url)
                return expected
        ctrl = DockerImageController(ExampleDockerImageAdapterInterface())
        ret = ctrl.create(expected.name, expected.description, expected.url)
        self.assertEqual(ret, expected)


class LabDockerImageControllerTestCase(unittest.TestCase):
    def test_init(self):
        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            pass
        expected = ExampleLabDockerImageAdapterInterface()
        ctrl = LabDockerImageController(expected)
        self.assertEqual(ctrl.adapter, expected)

    def test_create(self):
        this = self
        expected = LabDockerImage("8", "3", "4", "url")
        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            def create(self, lab_id: Identifier, docker_image_id: Identifier, docker_image_name: str) -> LabDockerImage:
                this.assertEqual(lab_id, expected.lab_id)
                this.assertEqual(docker_image_id, expected.docker_image_id)
                this.assertEqual(docker_image_name, expected.docker_image_name)
                return expected
        ctrl = LabDockerImageController(ExampleLabDockerImageAdapterInterface())
        ret = ctrl.create(expected.lab_id, expected.docker_image_id, expected.docker_image_name)
        self.assertEqual(ret, expected)


class LabControllerTestCase(unittest.TestCase):
    def test_init(self):
        class ExampleLabAdapterInterface(LabAdapterInterface):
            pass
        expected = ExampleLabAdapterInterface()
        ctrl = LabController(expected)
        self.assertEqual(ctrl.adapter, expected)

    def test_create(self):
        this = self
        expected = Lab("8", "lab", "lab", "desc")
        class ExampleLabAdapterInterface(LabAdapterInterface):
            def create(self, name: str, namespace_prefix: str, description: str) -> Lab:
                this.assertEqual(name, expected.name)
                this.assertEqual(namespace_prefix, expected.namespace_prefix)
                this.assertEqual(description, expected.description)
                return expected
        ctrl = LabController(ExampleLabAdapterInterface())
        ret = ctrl.create(expected.name, expected.namespace_prefix, expected.description)
        self.assertEqual(ret, expected)


class VirtualMachineInstanceControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy, self.registry = get_mocked_registry(self)

    def test_api(self):
        namespace_ctrl = NamespaceController(self.registry)

        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            pass

        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())

        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            pass

        lab_docker_image_ctrl = LabDockerImageController(ExampleLabDockerImageAdapterInterface())
        ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        self.assertIsInstance(ctrl._api(), VirtualMachineInstance)

    def test_create(self):
        this = self
        expected_docker_image = DockerImage("10", "name", "desc", "url")
        expected_lab_docker_image = LabDockerImage("1", "8", "10", "ubuntu")
        expected_namespace = "ns1"
        expected_template_data = {"cores": 3, "memory": "3G",
                                  "vm_image": expected_docker_image.url,
                                  "vmi_name": expected_lab_docker_image.docker_image_name,
                                  "namespace": expected_namespace}
        expected_data = "template"
        expected = "success"

        # Injected Controllers
        namespace_ctrl = NamespaceController(self.registry)

        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            def get(self, identifier: Identifier) -> DockerImage:
                this.assertEqual(identifier, expected_lab_docker_image.docker_image_id)
                return expected_docker_image

        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())

        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            pass

        lab_docker_image_ctrl = LabDockerImageController(ExampleLabDockerImageAdapterInterface())

        # Injected Api and Template
        class ExampleTemplateEngine(TemplateEngine):
            def replace_template(self, template: str, data: DataType, strict: bool = False) -> str:
                this.assertEqual(data, expected_template_data)
                return expected_data

        class ExampleApi:
            def create(self, namespace, data: str) -> str:
                this.assertEqual(namespace, expected_namespace)
                this.assertEqual(data, expected_data)
                return expected

        ctrl = VirtualMachineInstanceController(self.registry, namespace_ctrl=namespace_ctrl,
                                                docker_image_ctrl=docker_image_ctrl,
                                                lab_docker_image_ctrl=lab_docker_image_ctrl,
                                                template_engine=ExampleTemplateEngine())
        ctrl._api = lambda: ExampleApi()
        ret = ctrl.create(expected_namespace, expected_lab_docker_image)
        self.assertEqual(ret, expected)

    def test_get_list_of_lab_instance(self):
        this = self
        # Input Objects
        expected_lab_instance = LabInstance("1", "2", "3")
        expected_lab = Lab("4", "name", "pref", "desc")
        expected = "success"
        expected_namespace = \
            f"{expected_lab.namespace_prefix}-{expected_lab_instance.user_id}-{expected_lab_instance.primary_key}"

        # Injected Controllers
        class ExampleNamespaceApi:
            def get(self, identifier: str):
                this.assertEqual(identifier, expected_namespace)
                return ""

        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: ExampleNamespaceApi()

        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            pass

        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())

        class ExampleLabAdapterInterface(LabAdapterInterface):
            def get(self, identifier: Identifier) -> Lab:
                this.assertEqual(identifier, expected_lab_instance.lab_id)
                return expected_lab

        lab_ctrl = LabController(ExampleLabAdapterInterface())

        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            pass

        lab_docker_image_ctrl = LabDockerImageController(ExampleLabDockerImageAdapterInterface())

        # Injected Api and Template Engine
        class ExampleApi:
            def get_list(self, namespace):
                this.assertEqual(namespace, expected_namespace)
                return [expected]

        class ExampleTemplateEngine(TemplateEngine):
            pass

        # Create VMI Controller
        ctrl = VirtualMachineInstanceController(self.registry, namespace_ctrl=namespace_ctrl,
                                                docker_image_ctrl=docker_image_ctrl,
                                                lab_docker_image_ctrl=lab_docker_image_ctrl,
                                                template_engine=ExampleTemplateEngine())
        # Inject Api
        ctrl._api = lambda: ExampleApi()
        # Run Tests
        ret = ctrl.get_list_of_lab_instance(expected_lab_instance, lab_ctrl)
        self.assertListEqual(ret, [expected])

    def test_get_of_lab_instance(self):
        this = self
        # Input Objects
        expected_lab_instance = LabInstance("1", "2", "3")
        expected_lab = Lab("4", "name", "pref", "desc")
        expected_vmi_id = "2"
        expected = "success"
        expected_namespace = \
            f"{expected_lab.namespace_prefix}-{expected_lab_instance.user_id}-{expected_lab_instance.primary_key}"

        # Injected Controllers
        class ExampleNamespaceApi:
            def get(self, identifier: str):
                this.assertEqual(identifier, expected_namespace)
                return ""

        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: ExampleNamespaceApi()

        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            pass

        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())

        class ExampleLabDockerImageAdapterInterface(LabDockerImageAdapterInterface):
            pass

        lab_docker_image_ctrl = LabDockerImageController(ExampleLabDockerImageAdapterInterface())

        class ExampleLabAdapterInterface(LabAdapterInterface):
            def get(self, identifier: Identifier) -> Lab:
                this.assertEqual(identifier, expected_lab_instance.lab_id)
                return expected_lab

        lab_ctrl = LabController(ExampleLabAdapterInterface())

        # Injected Api and Template Engine
        class ExampleApi:
            def get(self, namespace, identifier):
                this.assertEqual(namespace, expected_namespace)
                this.assertEqual(identifier, expected_vmi_id)
                return expected

        class ExampleTemplateEngine(TemplateEngine):
            pass

        # Create VMI Controller
        ctrl = VirtualMachineInstanceController(self.registry, namespace_ctrl=namespace_ctrl,
                                                docker_image_ctrl=docker_image_ctrl,
                                                lab_docker_image_ctrl=lab_docker_image_ctrl,
                                                template_engine=ExampleTemplateEngine())
        # Inject Api
        ctrl._api = lambda: ExampleApi()
        # Run Tests
        ret = ctrl.get_of_lab_instance(expected_lab_instance, expected_vmi_id, lab_ctrl)
        self.assertEqual(ret, expected)


class LabInstanceControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy, self.registry = get_mocked_registry(self)

    def test_init(self):
        class ExampleLabInstanceAdapter(LabInstanceAdapterInterface):
            pass
        lab_instance_adapter = ExampleLabInstanceAdapter()
        user_ctrl = UserController(UserAdapterInterface())
        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        lab_ctrl = LabController(LabAdapterInterface())
        docker_image_ctrl = DockerImageController(DockerImageAdapterInterface())
        lab_docker_image_ctrl = LabDockerImageController(LabDockerImageAdapterInterface())
        vmi_ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        lab_instance_ctrl = LabInstanceController(
            adapter=lab_instance_adapter, virtual_machine_instance_ctrl=vmi_ctrl, namespace_ctrl=namespace_ctrl,
            lab_ctrl=lab_ctrl, network_policy_ctrl=network_policy_ctrl, user_ctrl=user_ctrl, secret_key="secret",
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        self.assertIsInstance(lab_instance_ctrl, LabInstanceController)

    def test_get_namespace_name(self):
        expected_lab = Lab("3", "name", "prefix", "desc")
        expected_lab_instance = LabInstance("8", "9", "10")
        expected_namespace_name = f"{expected_lab.namespace_prefix}-{expected_lab_instance.user_id}-{expected_lab_instance.primary_key}"
        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        lab_ctrl = LabController(LabAdapterInterface())

        def lab_ctrl_get(identifier):
            self.assertEqual(expected_lab_instance.lab_id, identifier)
            return expected_lab

        lab_ctrl.get = lab_ctrl_get
        namespace_name = LabInstanceController.get_namespace_name(expected_lab_instance, lab_ctrl)
        self.assertEqual(namespace_name, expected_namespace_name)

    def test_gen_namespace_name(self):
        expected_lab = Lab("3", "name", "prefix", "desc")
        expected_lab_instance = LabInstance("8", "9", "10")
        expected_namespace_name = f"{expected_lab.namespace_prefix}-{expected_lab_instance.user_id}-{expected_lab_instance.primary_key}"
        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        lab_ctrl = LabController(LabAdapterInterface())

        def lab_ctrl_get(identifier):
            self.assertEqual(expected_lab_instance.lab_id, identifier)
            return expected_lab

        lab_ctrl.get = lab_ctrl_get
        namespace_name = LabInstanceController.get_namespace_name(expected_lab_instance, lab_ctrl)
        self.assertEqual(namespace_name, expected_namespace_name)

    def test_create(self):
        this = self
        expected_lab_id = "3"
        expected_user_id = "5"
        expected_lab = Lab("3", "name", "prefix", "desc")
        expected_user = User("5")
        expected_lab_instance = LabInstance("6", "7", "8")
        expected_lab_docker_image_1 = LabDockerImage("1", "3", "4", "ubuntu")
        expected_lab_docker_image_2 = LabDockerImage("2", "3", "5", "arch")
        expected_namespace_name = f"{expected_lab.namespace_prefix}-{expected_user_id}-{expected_lab_instance.primary_key}"

        class ExampleLabInstanceAdapter(LabInstanceAdapterInterface):
            def create(self, lab_id: Identifier, user_id: Identifier) -> LabInstance:
                this.assertEqual(lab_id, expected_lab_id)
                this.assertEqual(user_id, expected_user_id)
                return expected_lab_instance

        lab_instance_adapter = ExampleLabInstanceAdapter()
        user_ctrl = UserController(UserAdapterInterface())

        def user_ctrl_get(identifier):
            self.assertEqual(identifier, expected_user_id)
            return expected_user

        user_ctrl.get = user_ctrl_get

        def namespace_ctrl_create(namespace_name):
            self.assertEqual(namespace_name, expected_namespace_name)
            return "success"

        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        namespace_ctrl.create = namespace_ctrl_create

        def network_policy_ctrl_create(namespace_name):
            self.assertEqual(namespace_name, expected_namespace_name)
            return "success"

        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        network_policy_ctrl.create = network_policy_ctrl_create

        def lab_ctrl_get(identifier):
            self.assertEqual(identifier, expected_lab_id)
            return expected_lab

        lab_ctrl = LabController(LabAdapterInterface())
        lab_ctrl.get = lab_ctrl_get
        docker_image_ctrl = DockerImageController(DockerImageAdapterInterface())

        lab_docker_image_ctrl = LabDockerImageController(LabDockerImageAdapterInterface())

        def lab_docker_image_filter(**kwargs):
            self.assertDictEqual({'lab_id': expected_lab.primary_key}, kwargs)
            return [expected_lab_docker_image_1, expected_lab_docker_image_2]

        lab_docker_image_ctrl.filter = lab_docker_image_filter

        counter = 0

        def vmi_ctrl_create(namespace_name, lab_docker_image):
            nonlocal counter
            counter += 1
            if counter == 1:
                self.assertEqual(namespace_name, expected_namespace_name)
                self.assertEqual(lab_docker_image, expected_lab_docker_image_1)
                return "success"
            else:
                self.assertEqual(namespace_name, expected_namespace_name)
                self.assertEqual(lab_docker_image, expected_lab_docker_image_2)
                return "success"

        vmi_ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        vmi_ctrl.create = vmi_ctrl_create
        lab_instance_ctrl = LabInstanceController(
            adapter=lab_instance_adapter, virtual_machine_instance_ctrl=vmi_ctrl, namespace_ctrl=namespace_ctrl,
            lab_ctrl=lab_ctrl, network_policy_ctrl=network_policy_ctrl, user_ctrl=user_ctrl, secret_key="secret",
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        lab_instance_kubernetes = lab_instance_ctrl.create(expected_lab_id, expected_user_id)
        self.assertIsInstance(lab_instance_kubernetes, LabInstanceKubernetes)
        self.assertEqual(expected_lab_id, lab_instance_kubernetes.lab_id)
        self.assertEqual(expected_user_id, lab_instance_kubernetes.user_id)
        self.assertEqual(expected_lab_instance.primary_key, lab_instance_kubernetes.primary_key)
        self.assertEqual(counter, 2)

    def test_delete(self):
        this = self
        expected_lab_id = "3"
        expected_user_id = "5"
        expected_lab = Lab("3", "name", "prefix", "desc")
        expected_lab_instance = LabInstance("6", "3", "5")
        expected_namespace_name = f"{expected_lab.namespace_prefix}-{expected_user_id}-{expected_lab_instance.primary_key}"

        class ExampleLabInstanceAdapter(LabInstanceAdapterInterface):
            def delete(self, identifier: Identifier) -> None:
                this.assertEqual(identifier, expected_lab_instance.primary_key)
                return None

        lab_instance_adapter = ExampleLabInstanceAdapter()

        def namespace_ctrl_delete(namespace_name):
            self.assertEqual(namespace_name, expected_namespace_name)
            return None

        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        namespace_ctrl.delete = namespace_ctrl_delete

        def lab_ctrl_get(identifier):
            self.assertEqual(identifier, expected_lab_id)
            return expected_lab

        lab_ctrl = LabController(LabAdapterInterface())
        lab_ctrl.get = lab_ctrl_get

        user_ctrl = UserController(UserAdapterInterface())
        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        docker_image_ctrl = DockerImageController(DockerImageAdapterInterface())
        lab_docker_image_ctrl = LabDockerImageController(LabDockerImageAdapterInterface())
        vmi_ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )

        ctrl = LabInstanceController(
            adapter=lab_instance_adapter, virtual_machine_instance_ctrl=vmi_ctrl, namespace_ctrl=namespace_ctrl,
            lab_ctrl=lab_ctrl, network_policy_ctrl=network_policy_ctrl, user_ctrl=user_ctrl, secret_key="secret",
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        ctrl.delete(expected_lab_instance)
        self.assertTrue(True)


    def test_get_list_of_user(self):
        this = self
        expected_lab_instance = LabInstance("2", "3", "1")
        expected_user = User("1")
        class ExampleLabInstanceAdapter(LabInstanceAdapterInterface):
            def filter(self, **kwargs: Dict[str, Any]) -> LabInstance:
                this.assertDictEqual(kwargs, {'user_id': expected_user.primary_key})
                return expected_lab_instance
        lab_instance_adapter = ExampleLabInstanceAdapter()
        namespace_ctrl = NamespaceController(self.registry)
        lab_ctrl = LabController(LabAdapterInterface())
        user_ctrl = UserController(UserAdapterInterface())
        network_policy_ctrl = NetworkPolicyController(self.registry)
        docker_image_ctrl = DockerImageController(DockerImageAdapterInterface())
        lab_docker_image_ctrl = LabDockerImageController(LabDockerImageAdapterInterface())
        vmi_ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )

        ctrl = LabInstanceController(
            adapter=lab_instance_adapter, virtual_machine_instance_ctrl=vmi_ctrl, namespace_ctrl=namespace_ctrl,
            lab_ctrl=lab_ctrl, network_policy_ctrl=network_policy_ctrl, user_ctrl=user_ctrl, secret_key="secret",
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        ret = ctrl.get_list_of_user(expected_user)
        self.assertEqual(ret, expected_lab_instance)

    def test_save(self):
        class ExampleLabInstanceAdapter(LabInstanceAdapterInterface):
            pass
        lab_instance_adapter = ExampleLabInstanceAdapter()
        user_ctrl = UserController(UserAdapterInterface())
        namespace_ctrl = NamespaceController(self.registry)
        namespace_ctrl._api = lambda: None
        network_policy_ctrl = NetworkPolicyController(self.registry)
        network_policy_ctrl._api = lambda: None
        lab_ctrl = LabController(LabAdapterInterface())
        docker_image_ctrl = DockerImageController(DockerImageAdapterInterface())
        lab_docker_image_ctrl = LabDockerImageController(LabDockerImageAdapterInterface())
        vmi_ctrl = VirtualMachineInstanceController(
            registry=self.registry, namespace_ctrl=namespace_ctrl, docker_image_ctrl=docker_image_ctrl,
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        lab_instance_ctrl = LabInstanceController(
            adapter=lab_instance_adapter, virtual_machine_instance_ctrl=vmi_ctrl, namespace_ctrl=namespace_ctrl,
            lab_ctrl=lab_ctrl, network_policy_ctrl=network_policy_ctrl, user_ctrl=user_ctrl, secret_key="secret",
            lab_docker_image_ctrl=lab_docker_image_ctrl
        )
        lab_instance = LabInstance("8", "9", "10")
        with self.assertRaises(Exception) as e:
            lab_instance_ctrl.save(lab_instance)
