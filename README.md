## The JSON Comparison package

[![Build Status](https://travis-ci.com/rugleb/JsonCompare.svg?branch=master)](https://travis-ci.com/rugleb/JsonCompare)
[![codecov](https://codecov.io/gh/rugleb/JsonCompare/branch/master/graph/badge.svg)](https://codecov.io/gh/rugleb/JsonCompare)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/jsoncomparison.svg)](https://badge.fury.io/py/jsoncomparison)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package is designed to compare two objects with a JSON-like structure and data types.

### Install

```
pip install -U pip jsoncomparison
```

### Usage

First you need to define two variables: expected & actual.
Think of them as the same variables that you use in unittests.

Expected - the original data object, that you want to see.
Actual - the given data object.

Then we will transfer these objects to check and identify the difference between them:

```python
from jsoncomparison import Compare, NO_DIFF


expected = {
    'project': {
        'name': 'jsoncomparison',
        'version': '0.1',
        'license': 'MIT',
        'language': {
            'name': 'python',
            'versions': [
                3.5,
                3.6
            ]
        }
    },
    'os': 'linux'
}

actual = {
    'project': {
        'name': 'jsoncomparison',
        'version': 0.1,
        'license': 'Apache 2.0',
        'language': {
            'name': 'python',
            'versions': [
                3.6
            ]
        }
    }
}

diff = Compare().check(expected, actual)
assert diff != NO_DIFF
```

The `check` method returns a dictionary of differences between `expected` and `actual` objects, and report about it.

Diff output:
```json
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
        }
    },
    "os": {
        "_message": "Key does not exists. Expected: <os>",
        "_expected": "os",
        "_received": null
    }
}
```

To check if the objects are the same, just call:

```python
diff = Compare().check(expected, actual)
self.assertEqual(diff, NO_DIFF)
```

### Configuration

The default configuration can be overridden by passing the config dictionary to the Compare class constructor.

Example:

```python
from jsoncomparison import Compare

config = {
    'output': {
        'console': False,
        'file': {
            'allow_nan': True,
            'ensure_ascii': True,
            'indent': 4,
            'name': None,
            'skipkeys': True,
        },
    },
    'types': {
        'float': {
            'allow_round': 2,
        },
        'list': {
            'check_length': True,
        }
    }
}

cmp = Compare(config)
```

### Output

By default, the configuration does not allow printing the comparison result to the console, but at the same time writes the results to a file.
These settings can be changed in your class config.

```py
config = {
    'output': {
        'console': True,
        'file': {}
    }
}
```

### Ignore rules

What if you do not want to compare some values and keys of objects from your JSON's?
In this case, you can define exception rules and pass them to the class constructor.

Let's go back to the example above:

```python
from jsoncomparison import Compare


expected = {
    # ...
}

actual = {
    # ...
}

rules = {
    'project': {
        'version': '*',
        'license': '*',
        'language': {
            'versions': {
                '_values': [
                    3.5
                ]
            }
        }
    },
    'os': '*',
}

diff = Compare(rules=rules).check(expected, actual)
assert diff == NO_DIFF
```

Now that we have added exceptions to the missing values,
the comparison test has been successfully passed!

### Links

You can see a more complex comparison example that I used to test the correct operation of an application:
[link](https://github.com/rugleb/jsoncomparison/blob/master/tests/test_compare.py#L84).
