import unittest

from jsoncompare.utils import is_dict, is_not_dict


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
