from copy import deepcopy


class Config:
    config = {}

    def __init__(self, config):
        self.config = config

    def get(self, path):
        keys = path.split('.')
        value = deepcopy(self.config)
        while keys and value is not None:
            value = value.get(keys.pop(0))
        return value

    def merge(self, config):
        self.config.update(config)
