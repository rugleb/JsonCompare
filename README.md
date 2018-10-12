## The JSON Comparison package

[![Build Status](https://travis-ci.com/rugleb/jsoncompare.svg?branch=master)](https://travis-ci.com/rugleb/jsoncompare)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package is designed for two objects with a JSON-like structure and data types.

### Installation

```
pip install jsoncomparison
```

### Quick start

```
from jsoncomparison import Compare


expected = {
    'project': {
        'name': 'jsoncomparison',
        'version': '0.1',
        'license': 'MIT',
        'language': {
            'name': 'python',
            'versions': [
                3.5,
                3.6,
            ],
        },
        'os': 'linux',
    },
},

actual = {
    'project': {
        'name': 'jsoncomparison',
        'version': 0.1,
        'license': 'Apache 2.0',
        'language': {
            'name': 'python',
            'versions': [
                3.6,
            ],
        },
    },
},

diff = Compare().check(expected, actual)
assert diff == {}
```

Diff output:
```
{
    "project": {
        "version": {
            "_message": "Types not equal. Expected: <str>, received: <float>",
            "_expected": "str",
            "_received": "float"
        },
        "license": {
            "_message": "Values not equal. Expected: <MIT>, received: <Apache 2.0>",
            "_expected": "MIT",
            "_received": "Apache 2.0"
        },
        "language": {
            "versions": {
                "_length": {
                    "_message": "Lengths not equal. Expected <2>, received: <1>",
                    "_expected": 2,
                    "_received": 1
                },
                "_content": {
                    "0": {
                        "_message": "Value not found. Expected <3.5>",
                        "_expected": 3.5,
                        "_received": null
                    }
                }
            }
        },
        "os": {
            "_message": "Key does not exists. Expected: <os>",
            "_expected": "os",
            "_received": null
        }
    }
}
```
