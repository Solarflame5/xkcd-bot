from pathlib import Path # for... finding the token file from relative path???
import json # Used to turn xkcd's comic .json into a python dictionary
import datetime # Used to format comic date for the embed timestamp
import re # Used to parse duckduckgo search results
import requests
import discord
from discord import app_commands


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


def findXkcdUrlFromNumber(command_input): # Generate the URL to scrape from the provided number # pylint: disable=invalid-name
    if command_input is None: # If no input has been given, scrape latest comic.
        xkcd_url = "https://www.xkcd.com/info.0.json"
    else:
        xkcd_num = int(command_input)
        xkcd_url = "https://www.xkcd.com/" + str(xkcd_num) + "/info.0.json"
    return xkcd_url

def findXkcdUrlFromText(command_input): # Generate URL from provided text by searching it in duckduckgo, this whole function is horrible and will be rewritten # pylint: disable=invalid-name
    ddg_url_template = "https://html.duckduckgo.com/html/?q=site:xkcd.com+"
    xkcd_regex = r"xkcd\.com\/\d+\/?/"
    ddg_url = ddg_url_template + command_input.replace(" ", "+")
    print("searching using url: " + ddg_url)
    ddg_results = requests.get(ddg_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"})
    # make the request with a real useragent so ddg doesn't block request(taken from my firefox)
    xkcd_url_raw = re.search(xkcd_regex, ddg_results.text).group(0)
    xkcd_url = "https://www." + xkcd_url_raw + "info.0.json"
    return xkcd_url

def scrapeXKCD(xkcd_url): # pylint: disable=invalid-name
    xkcd_json = requests.get(xkcd_url) # TEMPORARY! will switch to aiohttp
    if xkcd_json.status_code != 200:
        raise Exception("ComicNotFound")
    xkcd_raw = json.loads(xkcd_json.content) # parse json into dictionary
    date = datetime.datetime(int(xkcd_raw["year"]), int(xkcd_raw["month"]), int(xkcd_raw["day"]))
    # generate date object from comic year, month, and day
    xkcd_content = {
        "title": xkcd_raw["title"],
        "img": xkcd_raw["img"],
        "alt": xkcd_raw["alt"],
        "date": date,
        "url": "https://www.xkcd.com/" + str(xkcd_raw["num"])
    } # only return the needed content
    return xkcd_content

# Read bot token from "token.txt" in the same folder as "main.py"
token_path = Path(__file__).with_name("token.txt") # shamelessly stolen from stackoverflow
with token_path.open("r") as token_file: # Kazani told use with statement instead
    bot_token = token_file.read()

intents = discord.Intents.none() # bot only uses slash commands, no intents needed

client = Client(intents=intents)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.tree.command(name="xkcd", description="Send an xkcd comic in chat.")
@app_commands.describe(input="The comic's number or title")
async def sendComic(interaction: discord.Interaction, input: str=None): # pylint: disable=redefined-builtin, disable=invalid-name
    await interaction.response.defer(ephemeral=False, thinking=True)
    print("comic requested with input: " + str(input))
    try: # Check if input is a number or not
        xkcd_url = findXkcdUrlFromNumber(input) # Get xkcd URL using provided number
    except ValueError:
        print("input is not a number, searching with duckduckgo")
        try:
            xkcd_url = findXkcdUrlFromText(input) # Search for xkcd URL using DuckDuckGo
        except: # pylint: disable=bare-except
            print("comic not found, sending error message")
            error_embed = discord.Embed(
                title="Comic not found",
                description="The comic you tried to send was not found in the DuckDuckGo search.",
                colour=discord.Colour.from_rgb(200, 150, 150)
            )
            error_embed.set_footer(text="Search string: " + input)
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return
    try:
        requested_comic = scrapeXKCD(xkcd_url)
    except: # pylint: disable=bare-except
        print("invalid input, sending error message")
        error_embed = discord.Embed(
            title="Invalid input",
            description="The comic you tried to send does not exist.",
            colour=discord.Colour.from_rgb(200, 150, 150)
        )
        error_embed.set_footer(text="Input number: " + input)
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return
    print("returned url: " + xkcd_url)
    comic_embed = discord.Embed(
        title=requested_comic["title"], # Comic title
        description=requested_comic["alt"], # Comic hover text
        url=requested_comic["url"], # Comic URL
        timestamp=requested_comic["date"], # Comic date
        colour=discord.Colour.from_rgb(150, 168, 200) # xkcd.com's background color
    )
    comic_embed.set_image(url=requested_comic["img"])
    if input is None:
        comic_embed.set_footer(text="No input provided")
    else:
        comic_embed.set_footer(text="Input string: " + input)
    await interaction.followup.send(embed=comic_embed, ephemeral=False)

client.run(bot_token)
