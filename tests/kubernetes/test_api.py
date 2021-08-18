import unittest

from lab_orchestrator_lib.kubernetes.api import add_api_namespaced, NamespacedApi, _API_EXTENSIONS_NAMESPACED, \
    _API_EXTENSIONS_NOT_NAMESPACED, add_api_not_namespaced, NotNamespacedApi, Proxy, APIRegistry, Namespace, \
    VirtualMachineInstance, NetworkPolicy


class ExampleNamespacedApi(NamespacedApi):
    pass


class ExampleNotNamespacedApi(NotNamespacedApi):
    pass


class AddApiDecoratorTestCase(unittest.TestCase):
    def test_add_api_namespaced(self):
        new_cls = add_api_namespaced("example_namespaced_api")(ExampleNamespacedApi)
        self.assertEqual(new_cls, ExampleNamespacedApi)
        self.assertEqual(_API_EXTENSIONS_NAMESPACED.get("example_namespaced_api"), ExampleNamespacedApi)

    def test_add_api_not_namespaced(self):
        new_cls = add_api_not_namespaced("example_not_namespaced_api")(ExampleNotNamespacedApi)
        self.assertEqual(new_cls, ExampleNotNamespacedApi)
        self.assertEqual(_API_EXTENSIONS_NOT_NAMESPACED.get("example_not_namespaced_api"), ExampleNotNamespacedApi)


class RequestsMock:
    pass


class RequestsResponseMock:
    def __init__(self, text):
        self.text = text


class ProxyTestCase(unittest.TestCase):
    def test_init(self):
        base_uri = "example.com"
        service_account_token = "abc"
        cacert = "cacert"
        insecure_ssl = False
        proxy = Proxy(base_uri=base_uri, service_account_token=service_account_token, cacert=cacert,
                      insecure_ssl=insecure_ssl, requests_lib=RequestsMock)
        self.assertEqual(proxy.base_uri, base_uri)
        self.assertEqual(proxy.service_account_token, service_account_token)
        self.assertEqual(proxy.requests, RequestsMock)
        self.assertEqual(proxy.verify, cacert)

    def test_init_no_ca(self):
        base_uri = "example.com"
        service_account_token = "abc"
        cacert = None
        insecure_ssl = False
        proxy = Proxy(base_uri=base_uri, service_account_token=service_account_token, cacert=cacert,
                      insecure_ssl=insecure_ssl, requests_lib=RequestsMock)
        self.assertEqual(proxy.base_uri, base_uri)
        self.assertEqual(proxy.service_account_token, service_account_token)
        self.assertEqual(proxy.requests, RequestsMock)
        self.assertEqual(proxy.verify, True)

    def test_init_insecure(self):
        base_uri = "example.com"
        service_account_token = "abc"
        cacert = "cacert"
        insecure_ssl = True
        proxy = Proxy(base_uri=base_uri, service_account_token=service_account_token, cacert=cacert,
                      insecure_ssl=insecure_ssl, requests_lib=RequestsMock)
        self.assertEqual(proxy.base_uri, base_uri)
        self.assertEqual(proxy.service_account_token, service_account_token)
        self.assertEqual(proxy.requests, RequestsMock)
        self.assertEqual(proxy.verify, False)

    def test_get(self):
        test_base_uri = "localhost:8000"
        test_address = "/apis/namespace"
        test_uri = test_base_uri + test_address
        test_token = ""
        test_cacert = ""
        response_text = "response"

        def get_mock(uri, headers, verify):
            self.assertEqual(uri, test_uri)
            self.assertDictEqual(headers, {"Authorization": f"Bearer {test_token}"})
            self.assertEqual(verify, test_cacert)
            return RequestsResponseMock(response_text)
        RequestsMock.get = get_mock
        proxy = Proxy(base_uri=test_base_uri, service_account_token=test_token, cacert=test_cacert,
                      requests_lib=RequestsMock)
        response = proxy.get(test_address)
        self.assertEqual(response, response_text)

    def test_post(self):
        test_base_uri = "localhost:8000"
        test_address = "/apis/namespace"
        test_uri = test_base_uri + test_address
        test_token = ""
        test_cacert = ""
        response_text = "response"
        test_data = "api: v1\nname: unknown\n"

        def post_mock(uri, headers, verify, data):
            self.assertEqual(uri, test_uri)
            test_headers = {"Authorization": f"Bearer {test_token}", "Content-Type": "application/yaml"}
            self.assertDictEqual(headers, test_headers)
            self.assertEqual(verify, test_cacert)
            self.assertEqual(data, test_data)
            return RequestsResponseMock(response_text)
        RequestsMock.post = post_mock
        proxy = Proxy(base_uri=test_base_uri, service_account_token=test_token, cacert=test_cacert,
                      requests_lib=RequestsMock)
        response = proxy.post(test_address, test_data)
        self.assertEqual(response, response_text)

    def test_delete(self):
        test_base_uri = "localhost:8000"
        test_address = "/apis/namespace"
        test_uri = test_base_uri + test_address
        test_token = ""
        test_cacert = ""
        response_text = "response"

        def delete_mock(uri, headers, verify):
            self.assertEqual(uri, test_uri)
            test_headers = {"Authorization": f"Bearer {test_token}"}
            self.assertDictEqual(headers, test_headers)
            self.assertEqual(verify, test_cacert)
            return RequestsResponseMock(response_text)
        RequestsMock.delete = delete_mock
        proxy = Proxy(base_uri=test_base_uri, service_account_token=test_token, cacert=test_cacert,
                      requests_lib=RequestsMock)
        response = proxy.delete(test_address)
        self.assertEqual(response, response_text)


class APIRegistryTestCase(unittest.TestCase):
    def test_extensions(self):
        proxy = Proxy("/api", requests_lib=RequestsMock)
        registry = APIRegistry(proxy)
        self.assertIsInstance(registry.namespace, Namespace)
        self.assertIsInstance(registry.virtual_machine_instance, VirtualMachineInstance)
        self.assertIsInstance(registry.network_policy, NetworkPolicy)
