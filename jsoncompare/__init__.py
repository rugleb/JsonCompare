import os
import json
import copy

from .utils import *


class Compare:
    config = {}

    def __init__(self, config=None):
        self.set_config(config)

    def set_config(self, config=None):
        if config is None:
            self.set_default_config()
        self.config = config

    def set_default_config(self):
        directory = os.path.dirname(__file__)
        path = '{}/{}'.format(directory, 'data/config.json')
        with open(path, 'r') as fp:
            config = json.load(fp)
        self.set_config(config)

    def check(self, expected, actual):
        pass

    def diff(self, expected, actual):
        pass

    def report(self, diff):
        pass

    @classmethod
    def _prepare(cls, x):
        return copy.deepcopy(x)
