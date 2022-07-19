#!/bin/bash
set -e

curl https://f000.backblazeb2.com/file/rdcodex/status-backup.db > orchard/bot/status.db

poetry run python3 orchard/bot/bot.py orchard/bot/status.db
