import os
import json
import copy


class Compare:
    config = {}

    def __init__(self, config=None):
        self.set_config(config)

    def set_config(self, config=None):
        if config is None:
            config = self.get_default_config()
        self.config = config

    @classmethod
    def get_default_config(cls):
        path = os.path.dirname(__file__) + '/data/config.json'
        with open(path, 'r') as fp:
            return json.load(fp)

    def check(self, expected, actual):
        pass

    def diff(self, expected, actual):
        pass

    def report(self, diff):
        pass

    @classmethod
    def _prepare(cls, x):
        return copy.deepcopy(x)
