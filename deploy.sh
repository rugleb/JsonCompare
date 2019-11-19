#!/usr/bin/env bash

set -e

python setup.py sdist

twine upload dist/*

rm -rf build/ dist/ jsoncomparison.egg-info/
