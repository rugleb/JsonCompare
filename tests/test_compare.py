import unittest

from jsoncompare import Compare


class CompareTestCase(unittest.TestCase):

    def test_factory(self):
        c = Compare.make()
        self.assertIsInstance(c, Compare)

    def test_base_config_method(self):
        config = Compare.base_config()
        self.assertIsInstance(config, dict)
