import unittest

from lab_orchestrator_lib.template_engine import TemplateEngine, DataType

from lab_orchestrator_lib.kubernetes.api import Namespace, NetworkPolicy, VirtualMachineInstance

from lab_orchestrator_lib.model.model import User, DockerImage, Lab, Identifier, LabInstance

from lab_orchestrator_lib.controller.controller import UserController, NamespaceController, NetworkPolicyController, \
    DockerImageController, VirtualMachineInstanceController, LabController, LabInstanceController

from lab_orchestrator_lib.database.adapter import UserAdapterInterface, DockerImageAdapterInterface, \
    LabAdapterInterface, LabInstanceAdapterInterface
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


class VirtualMachineInstanceControllerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.proxy, self.registry = get_mocked_registry(self)

    def test_api(self):
        namespace_ctrl = NamespaceController(self.registry)
        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            pass
        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())
        ctrl = VirtualMachineInstanceController(self.registry, namespace_ctrl, docker_image_ctrl)
        self.assertIsInstance(ctrl._api(), VirtualMachineInstance)

    def test_create(self):
        this = self
        expected_docker_image = DockerImage("10", "name", "desc", "url")
        expected_lab = Lab("8", "name", "prefix", "desc", "9", "ubuntu")
        expected_namespace = "ns1"
        expected_template_data = {"cores": 3, "memory": "3G",
                                  "vm_image": expected_docker_image.url,
                                  "vmi_name": expected_lab.docker_image_name,
                                  "namespace": expected_namespace}
        expected_data = "template"
        expected = "success"

        # Injected Controllers
        namespace_ctrl = NamespaceController(self.registry)

        class ExampleDockerImageAdapterInterface(DockerImageAdapterInterface):
            def get(self, identifier: Identifier) -> DockerImage:
                this.assertEqual(identifier, expected_lab.docker_image_id)
                return expected_docker_image

        docker_image_ctrl = DockerImageController(ExampleDockerImageAdapterInterface())

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
                                                template_engine=ExampleTemplateEngine())
        ctrl._api = lambda: ExampleApi()
        ret = ctrl.create(expected_namespace, expected_lab)
        self.assertEqual(ret, expected)

    def test_get_list_of_lab_instance(self):
        this = self
        # Input Objects
        expected_lab_instance = LabInstance("1", "2", "3")
        expected_lab = Lab("4", "name", "pref", "desc", "9", "ubuntu")
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
        expected_lab = Lab("4", "name", "pref", "desc", "9", "ubuntu")
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
                                                template_engine=ExampleTemplateEngine())
        # Inject Api
        ctrl._api = lambda: ExampleApi()
        # Run Tests
        ret = ctrl.get_of_lab_instance(expected_lab_instance, expected_vmi_id, lab_ctrl)
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
        expected = Lab("8", "lab", "lab", "desc", "10", "ubuntu")
        class ExampleLabAdapterInterface(LabAdapterInterface):
            def create(self, name: str, namespace_prefix: str, description: str, docker_image_id: Identifier,
                       docker_image_name: str) -> Lab:
                this.assertEqual(name, expected.name)
                this.assertEqual(namespace_prefix, expected.namespace_prefix)
                this.assertEqual(description, expected.description)
                this.assertEqual(docker_image_id, expected.docker_image_id)
                this.assertEqual(docker_image_name, expected.docker_image_name)
                return expected
        ctrl = LabController(ExampleLabAdapterInterface())
        ret = ctrl.create(expected.name, expected.namespace_prefix, expected.description,
                          expected.docker_image_id, expected.docker_image_name)
        self.assertEqual(ret, expected)

