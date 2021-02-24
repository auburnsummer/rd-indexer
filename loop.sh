#!/bin/bash

while true
do
    (node lib/cli.js db/orchard.db conf/sources.yml || true) | tee /tmp/orchard.log
    if [ -s /tmp/orchard.log ]
    then
        cat /tmp/orchard.log | gist-paste -p -f "$(date).log" | python mkhook.py | curl -H 'Content-Type: application/json' -d@- ${WEBHOOK}
    fi
    echo "Sleeping for 15 minutes..."
    sleep 900
done
