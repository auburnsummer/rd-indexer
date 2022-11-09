# Litestream

I'm using [Litestream](https://litestream.io/) to handle persistence of the `status.db` file.

## Environment variables

 - `LITESTREAM_ON`: This is set to `true` to enable litestream. If false, the bot will not use it.
 - `B2_ACCESS_KEY` and `KEY_ID`: B2 info.
 - `LITESTREAM_DB`: The path to the db we want to replicate
 - `LITESTREAM_PATH`: The path on the B2 bucket to replicate it to

## usage

So if you put `LITESTREAM_ON=true`, the bot expects that there is something already there to first
restore from in the litestream.

This means that if a new instance of the bot with a new `status.db` is being set up, we have to
do some manual steps.

Basically, it's something like this, e.g. if the path is `test`

```
export B2_ACCESS_KEY=...
export KEY_ID=...
LITESTREAM_DB=<path to db> LITESTREAM_PATH=test litestream replicate -config orchard/bot/litestream.yml
```

It depends on the scenario, but if it's an empty `status.db`, we can actually just have a fully
empty sqlite database and that's enough, the bot will populate the tables on first run.

