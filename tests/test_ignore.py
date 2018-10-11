import os
import json
import unittest


class IgnoreTestCase(unittest.TestCase):
    obj = None
    rules = None

    def setUp(self):
        curr_dir = os.path.dirname(__file__)
        with open('{}/{}'.format(curr_dir, 'data/rules.json'), 'r') as fp:
            self.rules = json.load(fp)
        with open('{}/{}'.format(curr_dir, 'data/expected.json'), 'r') as fp:
            self.obj = json.load(fp)

    def test_ignore(self):
        pass


if __name__ == '__main__':
    unittest.main()
