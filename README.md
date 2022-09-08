# rd-indexer

This is a set of Python scripts that produce [api.rhythm.cafe](api.rhythm.cafe),
the backend for [rhythm.cafe](rhythm.cafe).

It consists of the following submodules:

 - [parse](./orchard/parse/README.md): parse the JSON dialect used in .rdlevel files
 - [vitals](./orchard/vitals/README.md): parse an .rdzip file and extract relevant metadata
 - [scan](./orchard/scan/README.md): Scrape various sources of levels and populate an SQLite
   database with the metadata of those levels
 - [bot](./orchard/bot/README.md): A Discord bot and API used for level management
 - [package](./orchard/package/README.md): Take the SQLite database from the scan step and
   produce a static Docker image serving that data via an API

A Github Actions task periodically runs the scan and deploys a new package. i.e. api.rhythm.cafe
is actually an entirely static deployment. The only way to change anything is to deploy a new
version of it.