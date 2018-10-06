import os
import json
import copy

from jsoncompare.errors import TypesNotEqual
from jsoncompare.differs import Int, Str, Bool, Dict, List, Diff, Float


class Compare:
    config = {}

    types = {
        int: Int,
        str: Str,
        bool: Bool,
        dict: Dict,
        list: List,
        float: Float,
    }

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
        e = self.prepare(expected)
        a = self.prepare(actual)
        return self.diff(e, a) == {}

    def diff(self, e, a):
        t = type(e)
        if not isinstance(a, t):
            return TypesNotEqual(e, a)
        obj = self.types.get(t, Diff)
        return obj.diff(e, a)

    def report(self, diff):
        pass

    @classmethod
    def prepare(cls, x):
        return copy.deepcopy(x)
