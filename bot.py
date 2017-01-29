from time import sleep
import requests
import discord
import random
import json
import os

# Add to server
# https://discordapp.com/oauth2/authorize?client_id=275050313529032706&scope=bot&permissions=0

# https://gist.github.com/hzsweers/8595628
# Get env variable(s) from Heroku
discord_token = os.environ["morty_discord_token"]
api_key = os.environ["yt_key"]
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention

    if message.content.startswith("!playlist"):
        await client.send_message(message.channel, "Getting links...\nCopy each line and send it again to get mee6 to add it:")
        to_send = ""
        playlist_link = message.content.split(" ")[1]
        print("{} asked for !playlist {}".format(user, playlist_link))
        
        playlist_id = playlist_link.split("list=")[1]
        req = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&fields=items%2Fsnippet%2FresourceId%2FvideoId&key={}".format(playlist_id, api_key)

        info = requests.get(req)
        ids = json.loads(info.text)

        sleep(5)
        for snippet in ids["items"]:
            video_id = snippet["snippet"]["resourceId"]["videoId"]
            to_send += "!add https://www.youtube.com/watch?v={}".format(video_id)

        await client.send_message(message.channel, to_send)

    elif message.content.startswith("!coinflip"):
        flip = random.radint(1, 2):
            if flip = 1:
                await client.send_message(message.channel, "Heads wins!")
            else:
                await client.send_message(message.channel, "Tails wins!")

    elif message.content.startswith("!coinflip"):
        die = random.randint(1, 6)
        await client.send_message(message.channel, "{} rolled {}".format(user, die))

@client.event
async def on_ready():
    print("Logged in as\n{}\n{}\n------".format(client.user.name, client.user.id))

client.run(discord_token)
