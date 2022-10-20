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

# usage

`poetry run python ./orchard/bot/bot.py <path to status db>`

This uses the Discord HTTP interactions API, so you then have to go to [the developer portal](https://discord.com/developers/applications)
and change the URL it's talking to to `{url}/interactions`. For local development, usage of
[ngrok](https://ngrok.com/) is suggested.

