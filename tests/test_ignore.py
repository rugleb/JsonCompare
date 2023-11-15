import unittest

from jsoncomparison.ignore import Ignore

from . import load_json


class IgnoreTestCase(unittest.TestCase):

    def test_listable_rules_usage(self):
        obj = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        rules = ['a', 'd', 'e']

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {
                'b': 2,
                'c': 3,
            },
        )

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
        self.assertEqual(
            obj, {
                'a': {'a': 1, 'c': 3},
                'b': {
                    'a': {'b': 2},
                    'c': 3,
                },
                'c': 3,
            },
        )

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
            '_list': ['a', 'c'],
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, [
                {'b': 2},
                {'b': 5},
            ],
        )

    def test_ignore_list_items_without_special_rule(self):
        obj = [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 4, 'b': 5, 'c': 6},
        ]
        rules = [{'a': "*", 'c': "*"}]

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, [
                {'b': 2},
                {'b': 5},
            ],
        )

    def test_ignore_list_object_with_special_rule(self):
        obj = {
            'a': {
                'b': [{
                    'd': 1,
                    'e': [{'f': {'g': 2, 'h': 3}}, {'f': {'g': 4, 'h': 5}}],
                    'i': 6,
                    'j': None,
                }],
            },
        }

        rules = {
            'a': {
                'b': {
                    '_list': {
                        'j': '*',
                        'e': {'_list': {'f': {'g': '*'}}},
                    },
                },
            },
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {
                'a': {
                    'b': [{
                        'd': 1,
                        'e': [{'f': {'h': 3}}, {'f': {'h': 5}}],
                        'i': 6,
                    }],
                },
            },
        )

    def test_ignore_list_object(self):
        obj = {
            'a': {
                'b': [{
                    'd': 1,
                    'e': [{'f': {'g': 2, 'h': 3}}, {'f': {'g': 4, 'h': 5}}],
                    'i': 6,
                    'j': None,
                }],
            },
        }

        rules = {
            'a': {
                'b': [{
                    'j': '*',
                    'e': [{'f': {'g': '*'}}],
                }],
            },
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {
                'a': {
                    'b': [{
                        'd': 1,
                        'e': [{'f': {'h': 3}}, {'f': {'h': 5}}],
                        'i': 6,
                    }],
                },
            },
        )

    def test_ignore_range(self):
        obj = {'a': 1.0}
        rules = {
            'a': {
                '_range': [0.9, 1.1],
            },
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {
                'a': True,
            },
        )

    def test_deep_analyzing(self):
        obj = load_json('ignore/object.json')
        rules = load_json('ignore/rules.json')
        expected = load_json('ignore/expected.json')

        obj = Ignore.transform(obj, rules)
        self.assertEqual(obj, expected)

    def test_regex_rules_usage(self):
        obj = {'a': 1, 'b': 'some_value_that_matches', 'c': 3, 'd': 4}

        rules = {
            'b': {'_re': '^some_va'},
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {'a': 1, 'c': 3, 'd': 4},
        )

    def test_regex_rules_usage_not_matching(self):
        obj = {'a': 1, 'b': "non_match_value", 'c': 3, 'd': 4}

        rules = {
            'b': {'_re': '^some_va'},
        }

        obj = Ignore.transform(obj, rules)
        self.assertEqual(
            obj, {'a': 1, 'b': 'non_match_value', 'c': 3, 'd': 4},
        )


if __name__ == '__main__':
    unittest.main()
