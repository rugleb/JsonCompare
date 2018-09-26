import json

from .utils import *


class Compare:

    _config = {}

    def __init__(self, config=None):
        self._config = self._set_up(config)

    def _set_up(self, config=None):
        default = self._default_config()
        return concat(default, config or {})

    @classmethod
    def _default_config(cls):
        path = '{dir}/data/config.json'.format(dir=directory(__file__))
        with open(path, 'r') as fd:
            return json.load(fd)

    @classmethod
    def make(cls, config=None):
        return cls(config)
