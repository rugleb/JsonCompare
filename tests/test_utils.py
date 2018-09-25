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

        self.assertFalse(is_dict([]))
        self.assertTrue(is_not_dict([]))

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

        self.assertFalse(is_bool(None))
        self.assertTrue(is_not_list(None))

    def test_is_list_function(self):
        self.assertTrue(is_list([]))
        self.assertFalse(is_not_list([]))

        self.assertFalse(is_list({}))
        self.assertTrue(is_not_list({}))

        self.assertFalse(is_list(1))
        self.assertTrue(is_not_list(1))

        self.assertFalse(is_list('str'))
        self.assertTrue(is_not_list('str'))

        self.assertFalse(is_list(True))
        self.assertTrue(is_not_list(True))

        self.assertFalse(is_list(None))
        self.assertTrue(is_not_list(None))

    def test_is_equal_types_function(self):
        self.assertTrue(is_equal_types({}, {}))
        self.assertTrue(is_equal_types([], []))
        self.assertTrue(is_equal_types(True, False))
        self.assertTrue(is_equal_types(None, None))
        self.assertTrue(is_equal_types('str', 'str'))

        self.assertFalse(is_equal_types(True, 1))
        self.assertTrue(is_not_equal_types(True, 1))

        self.assertFalse(is_equal_types(True, None))
        self.assertTrue(is_not_equal_types(True, None))

        self.assertFalse(is_equal_types({}, []))
        self.assertTrue(is_not_equal_types({}, []))

        self.assertFalse(is_equal_types('1', 1))
        self.assertTrue(is_not_equal_types('1', 1))

    def test_is_primitive_function(self):
        self.assertTrue(is_primitive(1))
        self.assertTrue(is_primitive(True))
        self.assertTrue(is_primitive('str'))

        self.assertTrue(is_not_primitive({}))
        self.assertTrue(is_not_primitive([]))
        self.assertTrue(is_not_primitive(None))
