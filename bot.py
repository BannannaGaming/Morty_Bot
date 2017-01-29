from platform import python_version
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

def add_to_playlist(req):
    global to_send
    async with aiohttp.get(req) as info:
        ids = await info.json()

    for snippet in ids["items"]:
        video_id = snippet["snippet"]["resourceId"]["videoId"]
        to_send += "!add https://www.youtube.com/watch?v={}\n".format(video_id)

@client.event
async def on_message(message):
    global to_send
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    try:
        if message.content.startswith("!playlist"):
            await client.send_message(message.channel, "Getting links...\nCopy each line and send it again to get mee6 to add it:")
            to_send = "```"
            playlist_link = message.content.split(" ")[1]
            print("{} asked for !playlist {}".format(user, playlist_link))  # Needed so I can see if a (large) playlist caused it to break

            playlist_id = playlist_link.split("list=")[1]
            add_to_playlist("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&fields=items%2Fsnippet%2FresourceId%2FvideoId&key={}".format(playlist_id, api_key))

            try:
                nextpagetoken = ids["nextPageToken"]
                add_to_playlist("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&fields=items%2Fsnippet%2FresourceId%2FvideoId&key={}".format(nextpagetoken, playlist_id, api_key))

            except KeyError:
                    pass  # No next page

            to_send += "```"  # Code block text so link thumbnails don't appear
            await client.send_message(message.channel, to_send)

        elif message.content.startswith("!coinflip"):
            flip = random.randint(1, 2)
            if flip == 1:
                await client.send_message(message.channel, "Heads wins :ok_hand:")
            else:
                await client.send_message(message.channel, "Tails wins :ok_hand:")

        elif message.content.startswith("!roll"):
            die = random.randint(1, 6)
            await client.send_message(message.channel, "{} rolled {}".format(user, die))

        elif message.content.startswith("!choice"):
            choices_str = message.content.split(" ", 1)[1]
            choices = choices_str.split(",")
            choice = random.randint(0, len(choices)-1)
            await client.send_message(message.channel, "I choose: {}".format(choices[choice]))

        elif message.content.startswith("!help"):
            await client.send_message(message.channel, "*Commands*:\n**!playlist**\n**!coinflip**\n**!roll**\n**!choice**\n**!help**")

        elif message.content.startswith("!info"):
            await client.send_message(message.channel, info_text)

    except (ValueError, IndexError, NameError, TypeError):
        print("Something went wrong :(")
        await client.send_message(message.channel, "Something went wrong :cry:")

@client.event
async def on_ready():
    print("Logged in as\n{}\n{}\n------".format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="with Rick <3"))

client.run(discord_token)
