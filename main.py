import discord
from discord import app_commands
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
    if xkcd_json.status_code != 200:
        raise Exception("ComicNotFound")
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

intents = discord.Intents.default()
intents.message_content = False

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@tree.command(name="xkcd", description="Send an xkcd comic in chat.")
@app_commands.describe(number="The comic's number")
async def sendComic(interaction: discord.Interaction, number: int=None):
    xkcd_url = findXkcdUrl(number)
    try:
        requested_comic = scrapeXKCD(xkcd_url)
    except:
        error_embed = discord.Embed(
            title="Invalid input", 
            description="The comic you tried to send does not exist.", 
            colour=discord.Colour.from_rgb(200, 150, 150)
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        return
    comic_embed = discord.Embed(
        title=requested_comic["title"], # Comic title
        description=requested_comic["alt"], # Comic hover text
        url=requested_comic["url"], # Comic URL
        timestamp=requested_comic["date"], # Comic date
        colour=discord.Colour.from_rgb(150, 168, 200) # xkcd.com's background color
    )
    comic_embed.set_image(url=requested_comic["img"])
    comic_embed.set_footer(text="Randall Munroe")
    await interaction.response.send_message(embed=comic_embed, ephemeral=False)

client.run(bot_token)