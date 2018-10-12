import unittest

from jsoncomparison.config import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config({
            'language': {
                'python': {
                    'version': [
                        3.5,
                        3.6,
                        3.7,
                    ],
                },
                'php': 7.2,
            },
            'os': 'linux',
        })

    def test_get_method(self):
        path = 'language.python.version'
        self.assertIsInstance(self.config.get(path), list)

        path = 'language.php'
        self.assertEqual(self.config.get(path), 7.2)

        path = 'os'
        self.assertEqual(self.config.get(path), 'linux')

    def test_merge_method(self):
        self.config.merge({'os': 'windows'})
        self.assertEqual(self.config.get('os'), 'windows')


if __name__ == '__main__':
    unittest.main()
