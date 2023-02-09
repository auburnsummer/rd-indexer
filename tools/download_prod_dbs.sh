#!/usr/bin/env bash

# For use in the "package" step, this script downloads the production orchard.db and status.db.

set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
cd $script_dir
cd ../orchard/package

wget https://f000.backblazeb2.com/file/rdsqlite/backups/status.db
wget --output-document orchard.db https://f000.backblazeb2.com/file/rdsqlite/backups/orchard-main.db 