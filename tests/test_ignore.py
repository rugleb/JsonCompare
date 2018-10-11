import os
import json
import unittest

from jsoncompare.ignore import Ignore


class IgnoreTestCase(unittest.TestCase):
    obj = None
    rules = None

    def setUp(self):
        curr_dir = os.path.dirname(__file__)
        with open('{}/{}'.format(curr_dir, 'data/rules.json'), 'r') as fp:
            self.rules = json.load(fp)
        with open('{}/{}'.format(curr_dir, 'data/expected.json'), 'r') as fp:
            self.obj = json.load(fp)

    def test_ignore_with_listable_rules(self):
        obj = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        rules = ['a', 'd', 'e']

        obj = Ignore(rules).transform(obj)
        self.assertEqual(obj, {
            'b': 2,
            'c': 3,
        })

    def test_ignore_with_dictable_rules(self):
        obj = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        rules = {'a': '*', 'd': '*', 'e': '*'}

        obj = Ignore(rules).transform(obj)
        self.assertEqual(obj, {
            'b': 2,
            'c': 3,
        })

    def test_ignore_with_sub_rule(self):
        obj = {
            'a': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            'b': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            'c': 3,
            'd': 4,
        }
        rules = {
            'a': ['b', 'd'],
            'b': {'b': '*', 'd': '*'},
            'd': '*',
        }

        obj = Ignore(rules).transform(obj)
        self.assertEqual(obj, {
            'a': {'a': 1, 'c': 3},
            'b': {'a': 1, 'c': 3},
            'c': 3,
        })


if __name__ == '__main__':
    unittest.main()
