class Config:
    def __init__(self, config: dict):
        self.config = config

    def get(self, path):
        value = self.config
        for key in path.split('.'):
            try:
                value = value.get(key, {})
            except AttributeError:
                return False
        return value

    def merge(self, config):
        self.config.update(config)
