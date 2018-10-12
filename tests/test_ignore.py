import unittest

from . import load_json
from jsoncomparison.ignore import Ignore


class IgnoreTestCase(unittest.TestCase):

    def test_listable_rules_usage(self):
        obj = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        rules = ['a', 'd', 'e']

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, {
            'b': 2,
            'c': 3,
        })

    def test_dictable_rules_usage(self):
        obj = {
            'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            'b': {
                'a': {'a': 1, 'b': 2},
                'b': 2,
                'c': 3,
            },
            'c': 3,
            'd': 4,
        }
        rules = {
            'a': ['b', 'd'],
            'b': {
                'a': ['a'],
                'b': '*',
            },
            'd': '*',
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, {
            'a': {'a': 1, 'c': 3},
            'b': {
                'a': {'b': 2},
                'c': 3,
            },
            'c': 3,
        })

    def test_ignore_values(self):
        obj = [1, 2, 3, 4]
        rules = {
            '_values': [1, 3],
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, [2, 4])

    def test_ignore_list_items(self):
        obj = [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6},
        ]
        rules = {
            '_list': ['a', 'c']
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, [
            {'b': 2},
            {'b': 5},
        ])

    def test_deep_analyzing(self):
        obj = load_json('ignore/object.json')
        rules = load_json('ignore/rules.json')
        expected = load_json('ignore/expected.json')

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, expected)


if __name__ == '__main__':
    unittest.main()
