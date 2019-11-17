#!/usr/bin/env bash

coverage run --source jsoncomparison -m unittest
coverage report -i -m
coverage html -d coverage/html
coverage xml -i -o coverage/index.xml
coverage erase
