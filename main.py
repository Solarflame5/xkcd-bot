import discord
from discord.ext import commands
import requests
import json # Used to turn xkcd's comic .json into a python dictionary
import datetime # Used to format comic date for the embed timestamp

def findXkcdUrl(command_input): # Generate the URL to scrape from the command input
    if command_input == None: # If no input has been given, scrape latest comic.
        xkcd_url = "https://www.xkcd.com/info.0.json"
    else:
        xkcd_num = int(command_input)
        xkcd_url = "https://www.xkcd.com/" + str(xkcd_num) + "/info.0.json"
    return xkcd_url

def scrapeXKCD(xkcd_url):
    xkcd_json = requests.get(xkcd_url) # TEMPORARY! will switch to aiohttp
    xkcd_raw = json.loads(xkcd_json.content) # parse json into dictionary
    date = datetime.datetime(int(xkcd_raw["year"]), int(xkcd_raw["month"]), int(xkcd_raw["day"])) # generate date
    xkcd_content = {
        "title": xkcd_raw["title"],
        "img": xkcd_raw["img"],
        "alt": xkcd_raw["alt"],
        "date": date,
        "url": "https://www.xkcd.com/" + str(xkcd_raw["num"])
    } # only return the needed content
    return xkcd_content

# Read bot token from "token.txt" in the same folder as "main.py"
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
    try: # Check if input is valid
        xkcd_url = findXkcdUrl(number)
    except ValueError:
        await comic.send("Invalid input, please only use\n```\n!xkcd\n!xkcd [number]\n```")
        return # Abort command if input is invalid
    requested_comic = scrapeXKCD(xkcd_url)
    comic_embed = discord.Embed(
        title=requested_comic["title"], # Comic title
        description=requested_comic["alt"], # Comic hover text
        url=requested_comic["url"], # Comic URL
        timestamp=requested_comic["date"], # Comic date
        colour=discord.Colour.from_rgb(150, 168, 200) # xkcd.com's background color
    )
    comic_embed.set_image(url=requested_comic["img"])
    comic_embed.set_footer(text="Randall Munroe")
    await comic.send(embed=comic_embed)

client.run(bot_token)