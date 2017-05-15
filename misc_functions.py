"""
misc_functions.py

Extra functions used in bot.py
"""

import urbandictionary as ud
import youtube_dl
import wikipedia
import datetime
import logging
import aiohttp
import json
import var

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
        return "{} cannot be found, you sick fuck".format(word)

async def search_wiki(search_req):
    try:
        page = wikipedia.page(search_req)
        wiki_def = var.wiki_msg.format(page.title, page.url, page.content[:1000])
        return wiki_def
    except wikipedia.exceptions.PageError:
        return "That does not match any Wikipedia pages"
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

# Test if URL will work with ytdl stream
# Code from https://github.com/rg3/youtube-dl/issues/4503#issuecomment-68356094
async def supported(url):
    ies = youtube_dl.extractor.gen_extractors()
    for ie in ies:
        if ie.suitable(url) and ie.IE_NAME != "generic":
            # Site has dedicated extractor
            return True
    return False

async def log(message, log_type):
    log_type(message)
    print(message)
