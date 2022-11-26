# bot

A discord bot that provides a management interface for levels.

# Background

The level database produced by [scan](../scan/README.md) and [vitals](../vitals/README.md) is
deterministic; that is, the data in it is entirely and only derived from the rdzip files itself.

However, there is still information about levels that is not based on the rdzip files, such as
when the level was indexed, or the peer review status of the level, etc.

This non-deterministic data is stored in a "status database", which is a seperate SQLite database
from the scan step. This bot is used to modify the status database. Eventually, this database is
read by the [package](../scan/README.md) step to produce the final api.rhythm.cafe package.

This bot package also provides a HTTP API. This API is currently only used for the peer review
workflow.

# Usage

`python -m orchard.bot <path to status db> <port>`

`<port> defaults to 8000 if not given.`

This uses the Discord HTTP interactions API, so you then have to go to [the developer portal](https://discord.com/developers/applications)
and change the URL it's talking to to `{url}/interactions` or `{url}/interactions2`. For local development, usage of
[ngrok](https://ngrok.com/) is suggested.

 > 💡 The `/interactions` and `/interactions2` are the same endpoint. Sometimes Discord caches
 > the DNS incorrectly, so you might have to change it to counteract this.

# Environment Variables


- `KEY_ID`: B2 key id. Used only if Litestream is enabled.
- `B2_ACCESS_KEY`: B2 application key. Used only if Litestream is enabled.
- `LITESTREAM_ON`: Set to `true` to enable Litestream
- `LITESTREAM_PATH`: path to the b2 bucket litestream should replicate from. Used only if Litestream is enabled.
- `BOT_TOKEN`: Discord bot token from the developer portal.
- `PUBLIC_KEY`: Discord public key from the developer portal.
- `APPLICATION_ID`: Discord application ID from the developer portal.
- `DEV_GUILD`: Name of guild the bot operates in. This bot is only designed to operate in a single guild.

- `SECRET_KEY_ORCH`: A 32 byte base64 encoded string. Used in peer review.
- `TYPESENSE_URL`: This should be `https://api.rhythm.cafe/typesense`

- `GITHUB_TOKEN`: A github access token. Used only for the `plsausage` command.

