# Discord XKCD bot
This bot automatically finds an [xkcd](https://xkcd.com/) from the given partial/full title and embeds it in chat
![Example screenshot](screenshots/example.png)
## Invite to your server
By clicking [here](https://discord.com/api/oauth2/authorize?client_id=978295243856285747&permissions=274877908992&scope=bot%20applications.commands) you can invite the version of the bot I'm hosting on my Raspberry Pi 1 B+ to your own server, the bot responds a bit slow when running on the Pi, so I recommend hosting the bot yourself instead of using my invite.
## Requirements for hosting
- [discord.py](https://github.com/Rapptz/discord.py)'s development version.
- [Requests](https://github.com/psf/requests)
## Setup
Create a text file called `token.txt` on the same directory as `main.py`, paste your bot's token inside this text file.

When running the bot for the first time, uncomment `await tree.sync()` under `async def on_ready():`, run the bot once and then comment the line again to register the `/xkcd` command.
## Usage
type `/xkcd [partial comic title]` or `/xkcd [comic number]` in chat.
## Reviews
"While xkcd-reading bots may be a massively oversaturated area with little to distinguish one bot from another, SolarFlame5's xkcd bot is unique in having been written by SolarFlame5." -[gollark](https://www.osmarks.net/)

"It could only be more perfect if it was written in Java." -Wyran

"Truly a bot that the founding fathers would be proud of." -Zach

"i'll review it tomorrow, rushing through a chemistry hw rn" -[Fishie](https://github.com/MuhammedAliSolkar)
## Disclaimer
This bot was a simple Python project I made for fun, It's not meant to be the best possible bot and has its own problems, here are some alternative bots made by some acquaintances of mine:
- https://github.com/SomeHybrid/xkcd-bot - Another bot written in Python.
- https://github.com/notdap/Xkcd-Bot - This bot is written in C# and uses a local database to get the comics which is faster.
- https://github.com/Neppkun/solarSucks.js - This one is written in JavaScript
