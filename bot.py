"""
This code sucks, you know it and I know it.
Async is hard...
Move on and call me an idiot later.
"""

from datetime import datetime as dt
import urbandictionary as ud
import wikipedia
import datetime
import aiohttp
import discord
import random
import json
import var

# Most send's have [:2000] to prevent going over message length limit

client = discord.Client()

# Quotes
with open ("quotes.txt", "r") as f:
    block_text = f.read()
    quotes = block_text.split("\n\n")


async def get_NEOs():
    current_dates = []
    now = datetime.datetime.now()
    today_date = now.strftime("%Y-%m-%d")

    async with aiohttp.get(var.NEO_link.format(today_date, var.nasa_api_key)) as info:
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

    return var.NEO_text.format(name, est_diameter, haz, close_approach_date, velocity, miss_distance)


# I blame Sam
async def dirty_stuff(search_term):
    words = []
    for word in search_term.split(" "):
        words.append(word)

    # %20 = URL formatting
    async with aiohttp.get(var.ph.format("%20".join(words))) as info:
        ph_link = await info.json()

    try:
        title = ph_link["videos"][0]["title"]
        views = ph_link["videos"][0]["views"]
        rating = ph_link["videos"][0]["rating"]
        dur = ph_link["videos"][0]["duration"]
        link = ph_link["videos"][0]["url"]
        return var.ph_text.format(title, views, rating, dur, link)

    except (IndexError, KeyError):
        return "{} cannot be found".format(word)


async def search_wiki(search_req):
    try:
        page = wikipedia.page(search_req)
        wiki_def = var.wiki_msg.format(page.title, page.url, page.content[:1000])
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
        return var.ud_msg.format(ud_name, ud_definition, ud_example)

    except NameError:
        return "Word not located in urban dictionary"


async def get_definition(words):  # Buggy
    async with aiohttp.get(var.define_word_url.format("%20".join(words))) as info:
        word_info = await info.json()
    try:
        definition = word_info["results"][0]["senses"][0]["definition"]  # Weird format
        defined = var.define_msg.format(words, definition[0])
        return defined

    except IndexError:
        return "{} cannot be found".format(word)


async def big(words):
    output = []
    for word in words.split(" "):
        for letter in word.lower():
            try:
                output.append(var.big_dict[letter])
            except KeyError:
                output.append(letter)

        # 2 spaces at request of Sam
        output.append("  ")
    return output


@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    try:

        # Bot owner / admin commands

        if message.content.lower().lower().startswith("!ping") and user in var.owner_approved:
            await client.send_message(message.channel, "pong")
            print("Ping from server: {}".format(message.server))

        elif message.content.lower().lower().startswith("!listservers") and user in var.owner_approved:
            servers = [server.name for server in client.servers]
            await client.send_message(message.channel, ", ".join(servers))

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

        elif message.content.lower().startswith("!yn "):
            yn = random.randint(1, 2)
            if yn == 1:
                await client.send_message(message.channel, "Yes")
            else:
                await client.send_message(message.channel, "No")

        elif message.content.lower().startswith("!numgen "):
            ran_str = message.content.split(" ", 1)[1]
            num1 = ran_str.split(",")[0]
            num2 = ran_str.split(",")[1]
            try:
                die = random.randint(int(num1), int(num2))
                await client.send_message(message.channel, "{} rolled {}".format(user, die))
            except (ValueError, TypeError):
                await client.send_message(message.channel, "Invalid number(s)")

        elif message.content.lower().startswith("!quote"):
                choice = random.randint(0, len(quotes)-1)
                await client.send_message(message.channel, quotes[choice])

        elif message.content.lower().startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message.content.lower().startswith("!wiki "):
            search_req = message.content.split(" ", 1)[1]
            wiki_to_send = await search_wiki(search_req)
            await client.send_message(message.channel, wiki_to_send)

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
            nasa_to_send = await get_NEOs()
            await client.send_message(message.channel, nasa_to_send)

        elif message.content.lower().startswith("!big "):
            words_to_big = message.content.split(" ", 1)[1]
            bigger_words = await big(" ".join(words_to_big))
            big_to_send = "".join(bigger_words)
            await client.send_message(message.channel, big_to_send)

        elif message.content.lower().startswith("!lads"):
            await client.send_message(message.channel, var.lads_text)

        elif message.content.lower().startswith("!info"):
            await client.send_message(message.channel, var.info_text)

        elif message.content.lower().startswith("!help"):
            await client.send_message(message.channel, var.help_message)

    except (ValueError, IndexError, NameError, TypeError):
        print("Something went wrong :(")
        await client.send_message(message.channel, "Something went wrong :cry:")


@client.event
async def on_ready():
    timestamp = dt.now().strftime("%H:%M")
    print("Logged in as\n{}\n{}\n@ {}\n------".format(client.user.name, client.user.id, timestamp))
    await client.change_presence(game=discord.Game(name="with Rick <3"))

client.run(var.discord_token)
