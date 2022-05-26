# NOTE: THIS CODE IS WORK IN PROGRESS, DO NOT USE THIS CODE, IT'S TERRIBLE

import discord
from discord.ext import commands
import requests
import json

def scrapeXKCD(xkcd_num = None):
    xkcd_url = None
    xkcd_json = None
    xkcd_raw = None
    xkcd = None
    if xkcd_num == None: # if no number has been given, scrape latest comic.
        xkcd_url = "https://www.xkcd.com/info.0.json"
    else:
        xkcd_url = "https://www.xkcd.com/" + str(xkcd_num) + "/info.0.json"
    xkcd_json = requests.get(xkcd_url) # TEMPORARY! will switch to aiohttp
    xkcd_raw = json.loads(xkcd_json.content) # parse json into dictionary
    xkcd_content = {
        "title": xkcd_raw["title"],
        "img": xkcd_raw["img"],
        "alt": xkcd_raw["alt"]
    } # only return the needed content
    return xkcd_content

# read bot token from "token.txt" in the same folder as "main.py"
token_file = open("token.txt")
bot_token = token_file.read()
token_file.close()

client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.command()
async def xkcd(comic, number=None):
    requested_comic = scrapeXKCD(number)
    await comic.send(embed=discord.Embed(title=requested_comic["title"], description=requested_comic["alt"]).set_image(url=requested_comic["img"]))

client.run(bot_token)
