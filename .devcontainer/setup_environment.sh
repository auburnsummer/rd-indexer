#!/usr/bin/env bash

# https://sharats.me/posts/shell-script-best-practices/

set -o errexit 
set -o nounset
set -o pipefail

if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./setup_environment.sh

Environment setup script for codespaces.

'
    exit
fi

cd "$(dirname "$0")"
cd ../

git lfs install
git lfs pull

poetry config virtualenvs.in-project true
poetry env use $(which pypy3)
poetry install