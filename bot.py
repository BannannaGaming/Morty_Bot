from imgur_album_link_xtractor import get_links
from platform import python_version
from sympy import *
import wikipedia
import platform
import aiohttp
import discord
import random
import os

# Add to server
# https://discordapp.com/oauth2/authorize?client_id=275050313529032706&scope=bot&permissions=0

# https://gist.github.com/hzsweers/8595628
# Get env variable(s) from Heroku
discord_token = os.environ["morty_discord_token"]
api_key = os.environ["yt_key"]

client = discord.Client()

to_send = ""
ids = ""

# sympy math things
x, y, a, b, z = symbols("x y a b z")

req_no_token = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=40&playlistId={}&fields=items(snippet(resourceId(playlistId%2CvideoId)))%2CnextPageToken&key={}"
req_with_token = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=40&pageToken={}&playlistId={}&fields=items(snippet(resourceId(playlistId%2CvideoId)))%2CnextPageToken&key={}"

help_message = """
***Commands***:
**!makelist** *Youtube playlist link*
**!coinflip**
**!roll**
**!choice** *Comma,Seperated,List,Of,Choices*
**!quote**
**!wiki** *page, such as "Donald Trump"*
**!imgurlinks** *album ID*
**!solve** *equation - must use x y a b z as symbols*
**!kys**
**!info**
**!help**"""

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

#  Message passed in so message.channel get be
async def add_to_playlist(channel, req, first=False):
    global ids
    to_send = "```"

    async with aiohttp.get(req) as info:
        ids = await info.json()

    for snippet in ids["items"]:
        video_id = snippet["snippet"]["resourceId"]["videoId"]
        to_send += "!add https://www.youtube.com/watch?v={}\n".format(video_id)

    to_send += "```"  # Code block text so link thumbnails don't appear
    await client.send_message(channel, to_send)

@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    try:
        if message.content.startswith("!makelist "):
            await client.send_message(message.channel, "Getting links...\nCopy each line and send it again to get mee6 to add it:")

            playlist_link = message.content.split(" ")[1]
            print("{} asked for !playlist {}".format(user, playlist_link))  # Needed so I can see if a (large) playlist caused it to break

            playlist_id = playlist_link.split("list=")[1]
            await add_to_playlist(message.channel, req_no_token.format(playlist_id, api_key), True)

            while 1:
                try:
                    nextpagetoken = ids["nextPageToken"]
                    print("Next page", nextpagetoken)
                    await add_to_playlist(message.channel, req_with_token.format(nextpagetoken, playlist_id, api_key))

                except KeyError:
                        break  # No next page

            await client.send_message(message.channel, "Finished retrieving playlist")

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
            with open ("quotes.txt", "r") as f:
                block_text = f.read()
                quotes = block_text.split("\n\n")
                choice = random.randint(0, len(quotes)-1)
                await client.send_message(message.channel, quotes[choice])

        elif message.content.startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message.content.startswith("!wiki "):
            search = message.content.split(" ", 1)[1]
            try:
                page = wikipedia.page(search)
                wiki_message = "`{} - {}`\n\n```{}...```".format(page.title, page.url, page.content[:1000])
                await client.send_message(message.channel, wiki_message)
            except wikipedia.exceptions.PageError:
                await client.send_message(message.channel, "That does not match any Wikipedia pages")
            except wikipedia.exceptions.DisambiguationError:
                await client.send_message(message.channel, "Multiple results found, try something else")

        elif message.content.startswith("!imgurlinks "):
            albumID = message.content.split(" ", 1)[1]
            links = "\n".join(await get_links(albumID))
            if links != "Error":
                for album_links in [links[i:i + 1800] for i in range(0, len(links), 1800)]:  # Split in to 1800 char chunks
                    await client.send_message(message.channel, album_links)
                await client.send_message(message.channel, "Finshed getting links")
            else:
                await client.send_message(message.channel, "Invalid album ID")

        elif message.content.startswith("!solve "):
            eq = message.content.split(" ", 1)[1]
            try:
                solved = solve(eq)
                await client.send_message(message.channel, "".join(solved))
            except (NameError, TypeError):
                await client.send_message(message.channel, "Incorrectly formatted request")

        elif message.content.startswith("!info"):
            await client.send_message(message.channel, info_text)

        elif message.content.startswith("!help"):
            await client.send_message(message.channel, help_message)

    except (ValueError, IndexError, NameError, TypeError):
        print("Something went wrong :(")
        await client.send_message(message.channel, "Something went wrong :cry:")

@client.event
async def on_ready():
    print("Logged in as\n{}\n{}\n------".format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="with Rick <3"))

client.run(discord_token)
