#!/bin/bash

while true
do
    (bash run.sh || true) | tee /tmp/orchard.log
    if [ -s /tmp/orchard.log ]
    then
        cat /tmp/orchard.log | gist -p -f "$(date).log" | python3 mkhook.py | curl -H 'Content-Type: application/json' -d@- ${WEBHOOK}
    fi
    echo "Sleeping for 15 minutes..."
    sleep 900
done
