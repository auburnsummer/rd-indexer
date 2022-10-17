set -x


overmind start -D -l typesense
sleep 1

# loop until the health endpoint indicates we're good to continue.
while : ; do
  sleep 1
  value=$(curl localhost:5000/health | jq ".ok")
  if [ X"$value" = "Xtrue" ] # constant prefix to allow $value to be an empty string.
  then
    break
  else
    echo "Health check false, waiting 1 second before trying again..."
  fi
done

# add collection...
curl "localhost:5000/collections" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "x-typesense-api-key: xyz" \
  -d @./schema.json

# add documents...
curl "localhost:5000/collections/levels/documents/import?action=create" \
  -X POST \
  -H "x-typesense-api-key: xyz" \
  --data-binary @./orchard.jsonl

# add the global search-only key.
curl 'localhost:5000/keys' \
    -X POST \
    -H "X-TYPESENSE-API-KEY: xyz" \
    -H 'Content-Type: application/json' \
    -d @./typesense-key.json

sleep 1
overmind stop typesense
overmind quit