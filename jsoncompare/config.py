class Config:
    config = {}

    def __init__(self, config):
        self.config = config

    def get(self, path):
        value = self.config
        for key in path.split('.'):
            value = value.get(key, {})
        return value or None

    def merge(self, config):
        self.config.update(config)
