from copy import deepcopy


class Config:
    config = {}

    def __init__(self, config: dict):
        self.config = config

    def get(self, path: str):
        keys = path.split('.')
        value = deepcopy(self.config)
        while keys and value is not None:
            value = value.get(keys.pop(0))
        return value
