from platform import python_version
import urbandictionary as ud
from sympy import *
import wikipedia
import platform
import aiohttp
import discord
import random
import os

# Most send's have [:2000] to prevent going over message length limit

# https://gist.github.com/hzsweers/8595628
# Get env variable(s) from Heroku
discord_token = os.environ["morty_discord_token"]
api_key = os.environ["yt_key"]

client = discord.Client()

# sympy math things
x, y, a, b, z = symbols("x y a b z")

# Quotes
with open ("quotes.txt", "r") as f:
    block_text = f.read()
    quotes = block_text.split("\n\n")

# Dictionary api
define_word_url = "http://api.pearson.com/v2/dictionaries/laes/entries?headword={}&limit=1"

# Help message
help_message = """
• **Search**
  • `!urban`  `word or phrase`
    • Search and show a definition and example from urbandictionary
  • `!wiki`  `wikipedia page, such as "Star Wars"`
    • Search and show a snippet of a given wikipedia page
  • `!define`  `word`
    • Search and show a definition of the given word

• **Maths**
  • `!solve`  `equation to solve`
    • Solve an equation such as `(x**2+7)*(x+1)` *(must only use x,y,a,b,z)*

• **Misc**
  • `!coinflip`
    • Heads or tails!
  • `!roll`
    • Returns a random number between 1 & 6
  • `!choice`  `Comma,Seperated,List,Of,Choices`
    • Pick a value from a given list of choices
  • `!quote`
    • Get a random Rick and Morty quote
  • `!info`
    • Get information about this bot
  • `!ping`
    • Am I online? - Currently only for verified users
  • `!help`
    • Shows this menu
"""

# Urban dictionary message
ud_msg = """
**{}**
```{}```
***Example***
```{}```"""

# Wikipedia message
wiki_msg = "**{}** - `{}`\n```{}```"

# Definition message
define_msg = "**{}**\n```{}```"

# Multi-line code block
info_text = """
```
- - - - Info - - - -
Python Version : {}
API Version    : {}
Platform       : {}
```
""".format(python_version(),
           discord.__version__,
           platform.system())


async def search_wiki(search_req):
    try:
        page = wikipedia.page(search_req)
        wiki_def = wiki_msg.format(page.title, page.url, page.content[:1000])
        return wiki_def

    except wikipedia.exceptions.PageError:
        return  "That does not match any Wikipedia pages"

    except wikipedia.exceptions.DisambiguationError:
        return "Multiple results found, try something else"


async def get_urban_def(word):
    try:
        defs = ud.define(word)
        for d in defs[:1]:  # Get first definition from generator
            ud_name =  d.word
            ud_definition = d.definition
            ud_example = d.example
        return ud_msg.format(ud_name, ud_definition, ud_example)

    except NameError:
        return "Word not located in urban dictionary"


async def get_definition(word):
    async with aiohttp.get(define_word_url.format(word)) as info:
        word_info = await info.json()
    try:
        definition = word_info["results"][0]["senses"][0]["definition"]  # Weird format
        defined = define_msg.format(word, definition[0])
        return defined

    except IndexError:
        return "{} cannot be found".format(word)


@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    try:
        # Stop random people spamming !ping with user check
        if message.content.startswith("!ping") and user == "<@263412940869206027>":
            await client.send_message(message.channel, "pong")

        elif message.content.startswith("!coinflip"):
            flip = random.randint(1, 2)
            if flip == 1:
                await client.send_message(message.channel, "Heads wins :ok_hand:")
            else:
                await client.send_message(message.channel, "Tails wins :ok_hand:")

        elif message.content.startswith("!roll"):
            die = random.randint(1, 6)
            await client.send_message(message.channel, "{} rolled {}".format(user, die))

        elif message.content.startswith("!choice "):
            choices_str = message.content.split(" ", 1)[1]
            choices = choices_str.split(",")
            choice = random.randint(0, len(choices)-1)
            await client.send_message(message.channel, "I choose: {}".format(choices[choice]))

        elif message.content.startswith("!quote"):
                choice = random.randint(0, len(quotes)-1)
                await client.send_message(message.channel, quotes[choice])

        elif message.content.startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message.content.startswith("!wiki "):
            search_req = message.content.split(" ", 1)[1]
            wiki_to_send = await search_wiki(search_req)
            await client.send_message(message.channel, wiki_to_send)

        elif message.content.startswith("!solve "):  # Needs improving
            eq = message.content.split(" ", 1)[1]
            try:
                solved = solve(eq)
                await client.send_message(message.channel, str(solved))
            except (NameError, TypeError):  # Doesent always catch? Testing needed
                await client.send_message(message.channel, "Incorrectly formatted request")

        elif message.content.startswith("!define "):
            word = message.content.split(" ", 1)[1]
            defined_to_send = await get_definition(word)
            await client.send_message(message.channel, defined_to_send[:2000])

        elif message.content.startswith("!urban "):
            ud_word = message.content.split(" ", 1)[1]
            ud_to_send = await get_urban_def(ud_word)
            await client.send_message(message.channel, ud_to_send[:2000])

        elif message.content.startswith("!info"):
            await client.send_message(message.channel, info_text)

        elif message.content.startswith("!help"):
            await client.send_message(message.channel, help_message)

    except (ValueError, IndexError, NameError, TypeError):
        print("Something went wrong :(")  # Debugging
        await client.send_message(message.channel, "Something went wrong :cry:")


@client.event
async def on_ready():
    print("Logged in as\n{}\n{}\n------".format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="with Rick <3"))


client.run(discord_token)
