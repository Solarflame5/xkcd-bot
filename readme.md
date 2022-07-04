# Discord XKCD bot
This bot scrapes an [xkcd](https://xkcd.com/) comic with the given number and sends it in chat
![Example screenshot](screenshots/example.png)
## Requirements
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

" ! The application did not respond
👁️ Only you can see this • Dismiss message" -[Fishie](https://github.com/MuhammedAliSolkar)
## Disclaimer
this is my first time making a discord bot and i know absolutely nothing about [discord.py](https://github.com/Rapptz/discord.py), feel free to criticise my code
