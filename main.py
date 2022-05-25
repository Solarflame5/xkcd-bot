# NOTE: THIS CODE IS WORK IN PROGRESS, DO NOT USE THIS CODE, IT'S TERRIBLE

import discord
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

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event # THIS IS ONLY TEMPORARY! DO NOT USE THIS
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!xkcd"):
        num = message.content[6:]
        await message.channel.send(scrapeXKCD(num)["img"])

client.run(bot_token)
