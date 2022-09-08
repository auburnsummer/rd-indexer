# bot

It's a discord bot!

The data is stored in a "status database", which is a seperate SQLite database from the scan
step.

# usage

`poetry run python ./orchard/bot/bot.py <path to status db>`

This uses the Discord HTTP interactions API, so you then have to go to [the developer portal](https://discord.com/developers/applications)
and change the URL it's talking to to `{url}/interactions`. For local development, usage of
[ngrok](https://ngrok.com/) is suggested.

