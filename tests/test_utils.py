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

    def test_is_int_function(self):
        self.assertTrue(is_int(1))
        self.assertFalse(is_not_int(1))

        self.assertFalse(is_int(True))
        self.assertTrue(is_not_int(True))

        self.assertFalse(is_int('1'))
        self.assertTrue(is_not_int('1'))

        self.assertFalse(is_int(None))
        self.assertTrue(is_not_int(None))

        self.assertFalse(is_int([]))
        self.assertTrue(is_not_int([]))

        self.assertFalse(is_int({}))
        self.assertTrue(is_not_int({}))

    def test_is_float_function(self):
        self.assertTrue(is_float(1.1))
        self.assertFalse(is_not_float(1.1))

        self.assertFalse(is_float('1.1'))
        self.assertTrue(is_not_float('1.1'))

        self.assertFalse(is_float(1))
        self.assertTrue(is_not_float(1))

        self.assertFalse(is_float(True))
        self.assertTrue(is_not_float(True))

        self.assertFalse(is_float(None))
        self.assertTrue(is_not_float(None))

        self.assertFalse(is_float({}))
        self.assertTrue(is_not_float({}))

        self.assertFalse(is_float([]))
        self.assertTrue(is_not_float([]))

    def test_is_str_function(self):
        self.assertTrue(is_str('1'))
        self.assertFalse(is_not_str('1'))

        self.assertFalse(is_str(1))
        self.assertTrue(is_not_str(1))

        self.assertFalse(is_str(True))
        self.assertTrue(is_not_str(True))

        self.assertFalse(is_str(None))
        self.assertTrue(is_not_str(None))

        self.assertFalse(is_str({}))
        self.assertTrue(is_not_str({}))

        self.assertFalse(is_str([]))
        self.assertTrue(is_not_str([]))

    def test_types_is_equal_function(self):
        self.assertTrue(types_is_equal({}, {}))
        self.assertTrue(types_is_equal([], []))
        self.assertTrue(types_is_equal(True, False))
        self.assertTrue(types_is_equal(None, None))
        self.assertTrue(types_is_equal('str', 'str'))

        self.assertFalse(types_is_equal(True, 1))
        self.assertTrue(types_is_not_equal(True, 1))

        self.assertFalse(types_is_equal(True, None))
        self.assertTrue(types_is_not_equal(True, None))

        self.assertFalse(types_is_equal({}, []))
        self.assertTrue(types_is_not_equal({}, []))

        self.assertFalse(types_is_equal('1', 1))
        self.assertTrue(types_is_not_equal('1', 1))

    def test_is_primitive_function(self):
        self.assertTrue(is_primitive(1))
        self.assertTrue(is_primitive(True))
        self.assertTrue(is_primitive('str'))

        self.assertTrue(is_not_primitive({}))
        self.assertTrue(is_not_primitive([]))
        self.assertTrue(is_not_primitive(None))

    def test_is_iterable_function(self):
        self.assertTrue(is_iterable([]))
        self.assertTrue(is_iterable({}))
        self.assertTrue(is_iterable(()))
        self.assertTrue(is_iterable(set()))

        self.assertTrue(is_not_iterable(1))
        self.assertTrue(is_not_iterable(True))
        self.assertTrue(is_not_iterable('str'))

    def test_key_exist_function(self):
        d = {'a': 1, 'b': 2}

        self.assertTrue(key_exist('a', d))
        self.assertTrue(key_not_exist('c', d))

        self.assertFalse(key_not_exist('a', d))
        self.assertFalse(key_exist('c', d))

    def test_values_equal_function(self):
        self.assertTrue(values_equal(1, 1))
        self.assertTrue(values_not_equal(1, '1'))
        self.assertTrue(values_not_equal(1, 1.1))
        self.assertTrue(values_not_equal(1, True))
        self.assertTrue(values_not_equal([], set([])))
        self.assertTrue(values_not_equal(False, None))
