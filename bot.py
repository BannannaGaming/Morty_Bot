from platform import python_version
from wordcloud import WordCloud
import urbandictionary as ud
from sympy import *
import matplotlib
import wikipedia
import platform
import datetime
import aiohttp
import discord
import random
import json
import os
matplotlib.use('Agg')  #  http://stackoverflow.com/a/41431428
import matplotlib.pyplot as plt

# Most send's have [:2000] to prevent going over message length limit

# https://gist.github.com/hzsweers/8595628
# Get env variable(s) from Heroku
discord_token = os.environ["morty_discord_token"]
yt_api_key = os.environ["yt_key"]
nasa_api_key = os.environ["nasa_key"]

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
`Commands not case sensetive`

• **Search**
  • `!urban`  `word or phrase`
    • Search and show a definition and example from urbandictionary
  • `!wiki`  `wikipedia page, such as "Star Wars"`
    • Search and show a snippet of a given wikipedia page
  • `!define`  `word`
    • Search and show a definition of the given word
  • `!ph` `search term`
    • :wink:

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
  • `!big`
    • Make text bigger
  • `!NEO`
    • Get the closest near earth object (uses NASA API)
  • `!wc`
    • Create a word cloud from all messages sent on this server `[only DGI server supported]`
  • `!info`
    • Get information about this bot
  • `!help`
    • Shows this menu

• **Bot Owner**
  • `!ping`
  • `!erasedict`
  • `!listservers`
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
- - - -  --  - - - -
```
Add me to another server : http://bit.ly/Morty-bot
Test me on my own server : https://www.discord.gg/kDE7HJy
My source code : https://github.com/thatguywiththatname/Morty_Bot
""".format(python_version(),
           discord.__version__,
           platform.system())

 # http://www.hubtraffic.com
ph = "http://www.pornhub.com/webmasters/search?id=44bc40f3bc04f65b7a35&ordering=mostviewed&period=weekly&thumbsize=small&search={}"

# Python because colours
ph_text = """
**{}**
```python
Views    : {}
Rating   : {}
Duration : {}```
{}
"""

# BIGGGG
big_dict = {
    "a":":regional_indicator_a:",
    "b":":regional_indicator_b:",
    "c":":regional_indicator_c:",
    "d":":regional_indicator_d:",
    "e":":regional_indicator_e:",
    "f":":regional_indicator_f:",
    "g":":regional_indicator_g:",
    "h":":regional_indicator_h:",
    "i":":regional_indicator_i:",
    "j":":regional_indicator_j:",
    "k":":regional_indicator_k:",
    "l":":regional_indicator_l:",
    "m":":regional_indicator_m:",
    "n":":regional_indicator_n:",
    "o":":regional_indicator_o:",
    "p":":regional_indicator_p:",
    "q":":regional_indicator_q:",
    "r":":regional_indicator_r:",
    "s":":regional_indicator_s:",
    "t":":regional_indicator_t:",
    "u":":regional_indicator_u:",
    "v":":regional_indicator_v:",
    "w":":regional_indicator_w:",
    "x":":regional_indicator_x:",
    "y":":regional_indicator_y:",
    "z":":regional_indicator_z:",
    "!":":exclamation:",
    "*":":asterisk:",
    "?":":question:",
    "#":":hash:",
    "1":":clock1:",
    "2":":clock2:",
    "3":":clock3:",
    "4":":clock4:",
    "5":":clock5:",
    "6":":clock6:",
    "7":":clock7:",
    "8":":clock8:",
    "9":":clock9:",
}

# NASA
NEO_link = "https://api.nasa.gov/neo/rest/v1/feed?start_date={}&api_key={}"
overview_link = "https://api.nasa.gov/neo/rest/v1/stats?&api_key={}"
NEO_text = """
**Name: {}**
```Estimated diameter: {} meters
Potentially hazardous? {}
Close approach date : {}
Velocity: {}mph
Miss distance: {} meters```"""

# Word cloud
word_dict = {}

async def get_NEOs():
    current_dates = []
    now = datetime.datetime.now()
    today_date = now.strftime("%Y-%m-%d")

    async with aiohttp.get(NEO_link.format(today_date, nasa_api_key)) as info:
        NEO_parsed = await info.json()

    for date in NEO_parsed["near_earth_objects"]:
        current_dates.append(date)
    if today_date in current_dates:
        info_date = str(today_date)
    else:
        info_date = str(min(current_dates))

    name = NEO_parsed["near_earth_objects"][info_date][0]["name"]
    diameter_min = NEO_parsed["near_earth_objects"][info_date][0]["estimated_diameter"]["meters"]["estimated_diameter_min"]
    diameter_max = NEO_parsed["near_earth_objects"][info_date][0]["estimated_diameter"]["meters"]["estimated_diameter_max"]
    est_diameter = diameter_max - diameter_min
    haz = NEO_parsed["near_earth_objects"][info_date][0]["is_potentially_hazardous_asteroid"]
    close_approach_date = NEO_parsed["near_earth_objects"][info_date][0]["close_approach_data"][0]["close_approach_date"]
    velocity = NEO_parsed["near_earth_objects"][info_date][0]["close_approach_data"][0]["relative_velocity"]["miles_per_hour"]
    miss_distance = NEO_parsed["near_earth_objects"][info_date][0]["close_approach_data"][0]["miss_distance"]["miles"]

    return NEO_text.format(name, est_diameter, haz, close_approach_date, velocity, miss_distance)

async def analyse(words):
    for word in words.split(" "):  # Splits the sentence into separate words
        if word not in word_dict: word_dict[word] = 1
        else:                     word_dict[word] += 1

async def create_wordcloud():
    if word_dict == {}:
        return "no words"

    alltext = ""  # Easier for wordcloud to read from 1 string

    for word in word_dict:
        count = word_dict[word]
        alltext += (word+" ")*count

    wordcloud = WordCloud().generate(alltext)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("wordcloud_fig")  # Always saved as this

# I blame Sam
async def dirty_stuff(search_term):
    words = []
    for word in search_term.split(" "):
        words.append(word)

    # %20 = URL formatting
    async with aiohttp.get(ph.format("%20".join(words))) as info:
        ph_link = await info.json()

    try:
        title = ph_link["videos"][0]["title"]
        views = ph_link["videos"][0]["views"]
        rating = ph_link["videos"][0]["rating"]
        dur = ph_link["videos"][0]["duration"]
        link = ph_link["videos"][0]["url"]
        return ph_text.format(title, views, rating, dur, link)

    except (IndexError, KeyError):
        return "{} cannot be found".format(word)


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


async def get_definition(word):  # Buggy
    async with aiohttp.get(define_word_url.format(word)) as info:
        word_info = await info.json()
    try:
        definition = word_info["results"][0]["senses"][0]["definition"]  # Weird format
        defined = define_msg.format(word, definition[0])
        return defined

    except IndexError:
        return "{} cannot be found".format(word)


async def big(words):
    output = []
    for word in words.split(" "):
        for letter in word.lower():
            try:
                output.append(big_dict[letter])
            except KeyError:
                output.append(letter)

        output.append(" ")
    return output


@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    try:
        await analyse(message.content)

        # Admin commands

        if message.content.lower().lower().startswith("!ping") and user == "<@263412940869206027>":
            await client.send_message(message.channel, "pong")
            print("Message server: {}".format(message.server))

        elif message.content.lower().lower().startswith("!erasedict") and user == "<@263412940869206027>":
            word_dict = {}
            await client.send_message(message.channel, "`word_dict` reset")

        elif message.content.lower().lower().startswith("!listservers") and user == "<@263412940869206027>":
            servers = []
            for server in client.servers:
                servers.append(server)
            await client.send_message(message.channel, servers)

        # Other commands

        elif message.content.lower().startswith("!coinflip"):
            flip = random.randint(1, 2)
            if flip == 1:
                await client.send_message(message.channel, "Heads wins :ok_hand:")
            else:
                await client.send_message(message.channel, "Tails wins :ok_hand:")

        elif message.content.lower().startswith("!roll"):
            die = random.randint(1, 6)
            await client.send_message(message.channel, "{} rolled {}".format(user, die))

        elif message.content.lower().startswith("!choice "):
            choices_str = message.content.split(" ", 1)[1]
            choices = choices_str.split(",")
            choice = random.randint(0, len(choices)-1)
            await client.send_message(message.channel, "I choose: {}".format(choices[choice]))

        elif message.content.lower().startswith("!quote"):
                choice = random.randint(0, len(quotes)-1)
                await client.send_message(message.channel, quotes[choice])

        elif message.content.lower().startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message.content.lower().startswith("!wiki "):
            search_req = message.content.split(" ", 1)[1]
            wiki_to_send = await search_wiki(search_req)
            await client.send_message(message.channel, wiki_to_send)

        elif message.content.lower().startswith("!solve "):  # Needs improving
            eq = message.content.split(" ", 1)[1]
            try:
                solved = solve(eq)
                await client.send_message(message.channel, str(solved))
            except (NameError, TypeError):  # Doesent always catch? Testing needed
                await client.send_message(message.channel, "Incorrectly formatted request")

        elif message.content.lower().startswith("!define "):
            word = message.content.split(" ", 1)[1]
            defined_to_send = await get_definition(word)
            await client.send_message(message.channel, defined_to_send[:2000])

        elif message.content.lower().startswith("!ph "):
            search = message.content.split(" ", 1)[1]
            ph_to_send = await dirty_stuff(search)
            await client.send_message(message.channel, ph_to_send)

        elif message.content.lower().startswith("!urban "):
            ud_word = message.content.split(" ", 1)[1]
            ud_to_send = await get_urban_def(ud_word)
            await client.send_message(message.channel, ud_to_send[:2000])

        elif message.content.lower().startswith("!neo"):
            nasa_to_send = get_NEOs()
            await client.send_message(message.channel, nasa_to_send)

        elif message.content.lower().startswith("!big "):
            words_to_big = message.content.split(" ", 1)[1]
            bigger_words = await big(" ".join(words_to_big))
            big_to_send = "".join(bigger_words)
            await client.send_message(message.channel, big_to_send)

        elif message.content.lower().startswith("!info"):
            await client.send_message(message.channel, info_text)

        elif message.content.lower().startswith("!help"):
            await client.send_message(message.channel, help_message)

        elif message.content.lower().startswith("!wc"):
            await client.send_message(message.channel, "Creating wordcloud...")
            response = await create_wordcloud()
            if response != "no words":
                await client.send_file(message.channel, "wordcloud_fig.png")#
            else:
                await client.send_message(message.channel, "No words!")

    except NameError:  # (ValueError, IndexError, NameError, TypeError)
        print("Something went wrong :(")  # Debugging
        await client.send_message(message.channel, "Something went wrong :cry:")


@client.event
async def on_ready():
    print("Logged in as\n{}\n{}\n------".format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="with Rick <3"))


client.run(discord_token)
