import unittest

from jsoncompare import Compare


class CompareTestCase(unittest.TestCase):

    def test_factory(self):
        c = Compare()
        self.assertIsInstance(c, Compare)
