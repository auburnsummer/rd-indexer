# package

Produce a Docker image that serves the data.

The package includes:

 - [Datasette](https://datasette.io/)
 - [Typesense](https://typesense.org/)

Which is served using the [Caddy](https://caddyserver.com/) server, currently deployed via
[fly.io](https://fly.io).

# usage

 1. Copy the database from the `scan` step into this directory
 2. Copy the status database from the bot into this directory
 3. run: `poetry run python ./package/package.py <path to scan database> <path to status database>`
 4. this produces a file called `orchard.jsonl` in this directory.
 5. use the Dockerfile to build the package.