# Discord XKCD bot
⚠️ Disclaimer: This bot is pretty bad and won't be updated anymore, consider using other bots available online. I might rewrite it as part of a general purpose bot later.
  
This bot automatically finds an [xkcd](https://xkcd.com/) from the given partial/full title and embeds it in chat
![Example screenshot](screenshots/example.png)
## Requirements for hosting
- [discord.py](https://github.com/Rapptz/discord.py)'s development version.
- [Requests](https://github.com/psf/requests)
## Setup
Create a text file called `token.txt` on the same directory as `main.py`, paste your bot's token inside this text file.

When running the bot for the first time, uncomment `await tree.sync()` under `async def on_ready():`, run the bot once and then comment the line again to register the `/xkcd` command.
## Usage
type `/xkcd [partial comic title]` or `/xkcd [comic number]` in chat.
