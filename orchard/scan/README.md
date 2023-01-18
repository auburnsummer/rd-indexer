# scan

This scans sources and adds them to a SQLite db. It needs a YAML definition of the sources
to scan, such as `sources.yml`.

# usage

`python ./orchard/scan/scan.py <path to db> <path to yml>`

The `ORCHARD_DEBUG` environment variable can be used to activate the debugger:

`ORCHARD_DEBUG=true python ./orchard/scan/scan.py <path to db> <path to yml>`