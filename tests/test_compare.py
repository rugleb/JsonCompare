import unittest

from jsoncompare import Compare, NO_DIFF, ValuesNotEqual, TypesNotEqual, KeyNotExist, \
    ValueNotFound, LengthsNotEqual


class CompareTestCase(unittest.TestCase):

    def test_compare_int(self):
        diff = Compare().check(1, 1)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(1, 2)
        self.assertEqual(diff, ValuesNotEqual(1, 2).explain())

    def test_compare_str(self):
        diff = Compare().check('str', 'str')
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check('str1', 'str2')
        self.assertEqual(diff, ValuesNotEqual('str1', 'str2').explain())

    def test_compare_float(self):
        diff = Compare().check(1.2, 1.2)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(1.23456, 1.23)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(1.2, 1.3)
        self.assertEqual(diff, ValuesNotEqual(1.2, 1.3).explain())

    def test_compare_bool(self):
        diff = Compare().check(True, True)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(True, False)
        self.assertEqual(diff, ValuesNotEqual(True, False).explain())

    def test_compare_dict_diff(self):
        e = {'int': 1, 'str': 'Hi', 'float': 1.23, 'bool': True}
        a = {'int': 2, 'str': 'Hi', 'float': 1}

        diff = Compare().check(e, e)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(e, a)
        self.assertEqual(diff, {
            'int': ValuesNotEqual(1, 2).explain(),
            'float': TypesNotEqual(1.23, 1).explain(),
            'bool': KeyNotExist('bool', None).explain()
        })

    def test_list_compare(self):
        e = [1.23, 2, 'three', True]
        a = [1.23, 3, 'three', False, None]

        diff = Compare().check(e, e)
        self.assertEqual(diff, NO_DIFF)

        diff = Compare().check(e, a)
        self.assertEqual(diff, {
            '_length': LengthsNotEqual(len(e), len(a)).explain(),
            '_content': {
                1: ValueNotFound(2, None).explain(),
                3: ValueNotFound(True, None).explain(),
            },
        })

    def test_prepare_method(self):
        e = [1, 2, 3, 4]
        p = Compare().prepare(e)

        self.assertTrue(e == p)
        self.assertFalse(e is p)


if __name__ == '__main__':
    unittest.main()
