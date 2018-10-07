import unittest

from jsoncompare import Compare


class CompareTestCase(unittest.TestCase):

    def test_factory(self):
        c = Compare()
        self.assertIsInstance(c, Compare)
        self.assertIsInstance(c.config, dict)

    def test_compare(self):
        e = {'int': 1, 'str': 'Hello, world', 'float': 1.2345, 'bool': True}
        a = {'int': 2, 'str': 'Hello, world', 'float': 1.23456, 'bool': False}
        diff = Compare().check(e, a)
        self.assertTrue('int' in diff)
        self.assertTrue('bool' in diff)
        self.assertTrue('str' not in diff)
        self.assertTrue('float' not in diff)
