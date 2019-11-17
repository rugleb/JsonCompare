#!/usr/bin/env bash

coverage run --source jsoncomparison -m unittest
coverage report -m -i
coverage html -d coverage/html
coverage erase
