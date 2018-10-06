import json

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
        with open('data/config.json', 'w') as fp:
            config = json.load(fp)
        self.set_config(config)
