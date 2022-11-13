#!/usr/bin/env bash

set -Eeuo pipefail

poetry config virtualenvs.in-project true
poetry env use $(which pypy3)
poetry install