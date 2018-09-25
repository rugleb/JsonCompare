import unittest

from jsoncompare.utils import *


class UtilsTestCase(unittest.TestCase):

    def test_is_dict_function(self):
        self.assertTrue(is_dict({}))
        self.assertFalse(is_not_dict({}))

        self.assertFalse(is_dict(1))
        self.assertTrue(is_not_dict(1))

        self.assertFalse(is_dict('str'))
        self.assertTrue(is_not_dict('str'))

        self.assertFalse(is_dict(True))
        self.assertTrue(is_not_dict(True))

        self.assertFalse(is_dict(None))
        self.assertTrue(is_not_dict(None))

    def test_is_bool_function(self):
        self.assertTrue(is_bool(True))
        self.assertTrue(is_bool(False))
        self.assertFalse(is_not_bool(True))
        self.assertFalse(is_not_bool(False))

        self.assertFalse(is_bool({}))
        self.assertTrue(is_not_bool({}))

        self.assertFalse(is_bool(1))
        self.assertTrue(is_not_bool(1))

        self.assertFalse(is_bool('str'))
        self.assertTrue(is_not_bool('str'))

        self.assertFalse(is_bool([]))
        self.assertTrue(is_not_bool([]))
