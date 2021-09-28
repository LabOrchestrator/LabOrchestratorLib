import unittest

from lab_orchestrator_lib.custom_exceptions import ValidationError

from lab_orchestrator_lib.model.model import check_dns_name, User, DockerImage, Model, LabDockerImage

dns_tests = [
    ("abc", True), ("a/b", False), ("aäb", False),
    ("def-", False), ("-def", False), ("d-ef", True),
    ("def.", False), (".def", False), ("d.ef", False),
    ("Abv", False), ("aBc", False), ("abC", False),
    ("8ab", False), ("ab8", True), ("a8b", True),
    ("", False), ("a" * 64, False), ("a" * 63, True)
]


class CheckDnsTestCase(unittest.TestCase):
    def test_dns(self):
        for name, expected in dns_tests:
            print(name, expected)
            self.assertEqual(check_dns_name(name), expected)


dns_subdomain_tests = [
    ("abc", True), ("a/b", False), ("aäb", False),
    ("def-", False), ("-def", False), ("d-ef", True),
    ("def.", False), (".def", False), ("d.ef", True),
    ("Abv", False), ("aBc", False), ("abC", False),
    ("8ab", True), ("ab8", True), ("a8b", True),
    ("", False), ("a" * 254, False), ("a" * 253, True)
]


class CheckDnsSubdomainTestCase(unittest.TestCase):
    def test_dns(self):
        for name, expected in dns_tests:
            print(name, expected)
            self.assertEqual(check_dns_name(name), expected)


class ModelTestCase(unittest.TestCase):
    def test_pk(self):
        tests = [
            ("", False), ("hallo", True), ("a" * 13, True), (8, True)
        ]
        for pk, expected in tests:
            print(pk, expected)
            if expected:
                self.assertIsInstance(Model(pk), Model)
            else:
                with self.assertRaises(ValidationError):
                    Model(pk)


class UserTestCase(unittest.TestCase):
    def test_pk(self):
        dns_tests = [
            ("abc", True), ("a/b", False), ("aäb", False),
            ("def-", False), ("-def", False), ("d-ef", True),
            ("def.", False), (".def", False), ("d.ef", False),
            ("Abv", False), ("aBc", False), ("abC", False),
            ("8ab", False), ("ab8", True), ("a8b", True),
            ("", False), ("a" * 13, False), ("a" * 12, True)
        ]
        for pk, expected in dns_tests:
            print(pk, expected)
            if expected:
                self.assertIsInstance(User(pk), User)
            else:
                with self.assertRaises(ValidationError):
                    User(pk)


class DockerImageTestCase(unittest.TestCase):
    def test_name(self):
        tests = [
            ("", False), ("hallo", True), ("a" * 33, False), ("a" * 32, True),
        ]
        for name, expected in tests:
            print(name, expected)
            if expected:
                self.assertIsInstance(DockerImage(1, name, "desc", "url"), DockerImage)
            else:
                with self.assertRaises(ValidationError):
                    DockerImage(1, name, "desc", "url")

    def test_desc(self):
        tests = [
            ("", False), ("hallo", True), ("a" * 129, False), ("a" * 128, True)
        ]
        for desc, expected in tests:
            print(desc, expected)
            if expected:
                self.assertIsInstance(DockerImage(1, "hi", desc, "url"), DockerImage)
            else:
                with self.assertRaises(ValidationError):
                    DockerImage(1, "hi", desc, "url")

    def test_url(self):
        tests = [
            ("", False), ("hallo", True), ("a" * 257, False), ("a" * 256, True)
        ]
        for url, expected in tests:
            print(url, expected)
            if expected:
                self.assertIsInstance(DockerImage(1, "hi", "desc", url), DockerImage)
            else:
                with self.assertRaises(ValidationError):
                    DockerImage(1, "hi", "desc", url)


class LabDockerImageTestCase(unittest.TestCase):
    def test_docker_image_name(self):
        for name, expected in dns_subdomain_tests:
            print(name, expected)
            if expected:
                self.assertIsInstance(LabDockerImage(1, 1, 1, name), LabDockerImage)
            else:
                with self.assertRaises(ValidationError):
                    LabDockerImage(1, 1, 1, name)

