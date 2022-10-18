# RD Indexer

This is a set of Python scripts that produce [api.rhythm.cafe](https://api.rhythm.cafe),
the backend for [rhythm.cafe](https://rhythm.cafe).

It consists of the following parts:

 - [parse](./orchard/parse/README.md): parse the JSON dialect used in .rdlevel files
 - [vitals](./orchard/vitals/README.md): parse an .rdzip file and extract relevant metadata
 - [scan](./orchard/scan/README.md): Scrape various sources of levels and populate an SQLite
   database with the metadata of those levels
 - [bot](./orchard/bot/README.md): A Discord bot and API used for level management
 - [package](./orchard/package/README.md): Take the SQLite database from the scan step and
   produce a static Docker image serving that data via an API

A Github Actions task periodically runs the scan and deploys a new package. Thus, `api.rhythm.cafe`
is actually an entirely static deployment. The only way to change anything is to deploy a new
version of it.

# Install

This repo uses Python 3.8+, and Poetry to define dependencies. Each submodule shares a single
dependency lockfile.

 1. Install poetry via [these directions](https://python-poetry.org/docs/#installation)
 2. Run `poetry install` in the root directory of this repo.
 3. Either use `poetry run` when running scripts, or do `poetry shell` to enter the virtual environment first.


# Usage

Refer to individual README files in each submodule. 