import unittest

from jsoncomparison import (
    NO_DIFF,
    Compare,
    KeyNotExist,
    LengthsNotEqual,
    TypesNotEqual,
    ValueNotFound,
    ValuesNotEqual,
)
from jsoncomparison.errors import UnexpectedKey

from . import load_json


class CompareTestCase(unittest.TestCase):

    def setUp(self):
        self.config = load_json('compare/config.json')
        self.compare = Compare(self.config)

    def test_compare_int(self):
        diff = self.compare.check(1, 1)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(1, 2)
        self.assertEqual(diff, ValuesNotEqual(1, 2).explain())

    def test_compare_str(self):
        diff = self.compare.check('str', 'str')
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check('str1', 'str2')
        self.assertEqual(diff, ValuesNotEqual('str1', 'str2').explain())

    def test_compare_float(self):
        diff = self.compare.check(1.2, 1.2)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(1.23456, 1.23)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(1.2, 1.3)
        self.assertEqual(diff, ValuesNotEqual(1.2, 1.3).explain())

    def test_compare_bool(self):
        diff = self.compare.check(True, True)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(True, False)
        self.assertEqual(diff, ValuesNotEqual(True, False).explain())

    def test_compare_dict_diff(self):
        e = {'int': 1, 'str': 'Hi', 'float': 1.23, 'bool': True}
        a = {'int': 2, 'str': 'Hi', 'float': 1}

        diff = self.compare.check(e, e)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(e, a)
        self.assertEqual(
            diff, {
                'int': ValuesNotEqual(1, 2).explain(),
                'float': TypesNotEqual(1.23, 1).explain(),
                'bool': KeyNotExist('bool', None).explain(),
            },
        )

    def test_compare_dict_diff_unexpected(self):
        e = {'int': 2, 'str': 'Hi', 'float': 1}
        a = {'int': 1, 'str': 'Hi', 'float': 1.23, 'bool': True}

        diff = self.compare.check(e, a)
        self.assertEqual(
            diff, {
                'int': ValuesNotEqual(2, 1).explain(),
                'float': TypesNotEqual(1, 1.23).explain(),
                'bool': UnexpectedKey(None, 'bool').explain(),
            },
        )

    def test_list_compare(self):
        e = [1.23, 2, 'three', True]
        a = [1.23, 3, 'three', False, None]

        diff = self.compare.check(e, e)
        self.assertEqual(diff, NO_DIFF)

        diff = self.compare.check(e, a)
        self.assertEqual(
            diff, {
                '_length': LengthsNotEqual(len(e), len(a)).explain(),
                '_content': {
                    1: ValueNotFound(2, None).explain(),
                    3: ValueNotFound(True, None).explain(),
                },
            },
        )

    def test_prepare_method(self):
        e = [1, 2, 3, 4]
        p = self.compare.prepare(e)

        self.assertTrue(e == p)
        self.assertTrue(e is not p)

    def test_compare_deep_data(self):
        rules = load_json('compare/rules.json')
        actual = load_json('compare/actual.json')
        expected = load_json('compare/expected.json')

        diff = Compare(self.config, rules).check(expected, actual)
        self.assertEqual(diff, NO_DIFF)

    def test_simple_list_with_dicts(self):
        expected = [
            {'a': "xxx"},
            {'a': "yyy"},
        ]
        actual = [
            {'a': "zzz"},
            {'a': "yyy"},
        ]
        diff = Compare().check(expected, actual)
        self.assertEqual(
            diff, {
                '_content': {
                    0: {'a': ValuesNotEqual('xxx', 'zzz').explain()},
                },
            },
        )

    # The next two tests represent some current behaviour that probably
    # is incorrect so they are left here as documentation for future changes
    # See https://github.com/rugleb/JsonCompare/pull/37#issuecomment-1821786007

    def test_list_with_dicts(self):
        expected = [
            {'a': "xxx"},
            {'a': "iii"},
            {'a': "yyy"},
            {'a': "jjj"},
        ]
        actual = [
            {'a': "zzz"},
            {'a': "yyy"},
            {'a': "xxx"},
            {'a': "eee"},
        ]
        diff = Compare().check(expected, actual)
        self.assertEqual(
            diff, {
                '_content': {
                    1: {'a': ValuesNotEqual('iii', 'zzz').explain()},
                    3: {'a': ValuesNotEqual('jjj', 'zzz').explain()},
                },
            },
        )

    def test_list_with_dicts_with_duplicates(self):
        expected = [
            {'a': "xxx"},
            {'a': "iii"},
            {'a': "xxx"},
            {'a': "jjj"},
        ]
        actual = [
            {'a': "zzz"},
            {'a': "iii"},
            {'a': "xxx"},
            {'a': "iii"},
        ]
        diff = Compare().check(expected, actual)
        self.assertEqual(
            diff, {
                '_content': {
                    3: {'a': ValuesNotEqual('jjj', 'zzz').explain()},
                },
            },
        )


if __name__ == '__main__':
    unittest.main()
