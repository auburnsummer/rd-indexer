#!/bin/bash

# make a copy of the original orchard.db:
cp db/orchard.db db/orchard_old.db

# now run the command...
node lib/cli.js db/orchard.db conf/sources.yml

# if there is a difference:
if [ $(sqldiff db/orchard.db db/orchard_old.db | wc -c) -ne 0 ]
then
	echo "Change made, let's upload it..."
	datasette publish fly db/orchard.db --app="orchard"
else
	echo "No change, leave it alone."
fi
