# XKCD Discord bot 
## Purpose
The bot uses [XKCD](https://xkcd.com/)'s api to retrieve a specific comic and send it to chat 
## Setup
#### Bare Metal
```bash
pip install --no-cache-dir -r requirements.txt
python3 main.py 
```
#### Docker
```bash
docker build -t xkcd_bot .
docker-compose up
```

## Usage
Type `!xkcd` to get the latest comic or `!xkcd [number]` to get a specific one. 
## Disclaimer
This is my first time making a discord bot and I know absolutely nothing about [discord.py](https://github.com/Rapptz/discord.py), feel free to criticise my code
