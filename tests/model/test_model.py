import unittest

from lab_orchestrator_lib.custom_exceptions import ValidationError

from lab_orchestrator_lib.model.model import check_dns_name, User, DockerImage, Model

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
