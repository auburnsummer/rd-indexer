set -x

overmind start -f ../Procfile -D -l meili
sleep 1

wait_on_iid() {
  while : ; do
    value=$(curl localhost:7700/tasks/$1 | jq ".status")
    if [ X"$value" = "X\"succeeded\"" ] # constant prefix to allow $value to be an empty string.
    then
      break
    else
      echo "Task still completing..."
    fi
    sleep 1
  done
  return 0
}

# loop until the health endpoint indicates we're good to continue.
while : ; do
  value=$(curl localhost:7700/health | jq ".status")
  if [ X"$value" = "X\"available\"" ] # constant prefix to allow $value to be an empty string.
  then
    break
  else
    echo "Health check false, waiting 1 second before trying again..."
  fi
  sleep 1
done

# setup index
task_uid=$(curl "localhost:7700/indexes" \
  -X POST \
  -H "Content-Type: application/json" \
  -d @./index.json | jq ".taskUid")

wait_on_iid $task_uid

# change settings of index
task_uid=$(curl "localhost:7700/indexes/levels/settings" \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d @./settings.json | jq ".taskUid")

wait_on_iid $task_uid

# add documents
task_uid=$(curl "localhost:7700/indexes/levels/documents" \
  -X POST \
  -H "Content-Type: application/x-ndjson" \
  -d @../orchard.ndjson | jq ".taskUid")

wait_on_iid $task_uid

# we're done here
overmind stop meili
overmind quit

# lastly, overwrite the meili instance id to a known value.
# so that each rebuild we have the same UID.
# mostly just for fun, but also if we want to GDPR our data after.

echo -n "99c0ffee-cafe-4444-9999-cafecafecafe" > /etc/meili/data.ms/instance-uid