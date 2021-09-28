import unittest

from lab_orchestrator_lib.custom_exceptions import ValidationError

from lab_orchestrator_lib.model.model import check_dns_name, User, DockerImage, Model

dns_tests = [
    ("abc", True), ("a/b", False), ("aäb", False),
    ("def-", False), ("-def", False), ("d-ef", True),
    ("Abv", False), ("aBc", False), ("abC", False),
    ("8ab", False), ("ab8", True), ("a8b", True),
    ("", False)
]


class CheckDnsTestCase(unittest.TestCase):
    def test_dns(self):
        for name, expected in dns_tests:
            print(name, expected)
            self.assertEqual(check_dns_name(name), expected)
