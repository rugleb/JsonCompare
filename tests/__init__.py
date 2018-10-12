import os
import json


def load_json(file):
    d = os.path.dirname(__file__)
    with open('{}/data/{}'.format(d, file), 'r') as fp:
        return json.load(fp)
