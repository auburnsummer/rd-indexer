#!/bin/bash
set -e

ls

cat ./orchard/bot/litestream.yaml

# Restore the database if it does not already exist.
if [ -f "./orchard/bot/status.db" ]; then
	echo "Database already exists, skipping restore"
else
	echo "No database found, restoring from replica if exists"
	litestream restore -v -config "./orchard/bot/litestream.yaml" -if-replica-exists "./orchard/bot/status.db"
fi

# Run litestream with your app as the subprocess.
exec litestream replicate -config "./orchard/bot/litestream.yaml" -exec "poetry run python3 orchard/bot/bot.py orchard/bot/status.db"