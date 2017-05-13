"""
This code sucks, you know it and I know it.
Async is hard...
Move on and call me an idiot later.
"""

from datetime import datetime as dt
import misc_functions
import youtube_dl
import concurrent
import discord
import random
import var

# Some send's have [:2000] to prevent going over message length limit

client = discord.Client()

# Quotes
with open("Text_Resources/quotes.txt", "r") as f:
    block_text = f.read()
    quotes = block_text.split("\n\n")

# Insults/Roasts
with open("Text_Resources/roasts.txt", "r") as f:
    block_text = f.read()
    insults = block_text.split("\n\n")

@client.event
async def on_message(message):
    if message.author == client.user:  # Don't reply to self
        return
    else:
        user = "{0.author.mention}".format(message)  # Get user mention
        user_voice_channel = message.author.voice.voice_channel
        user_server = message.server
        message_content_lower = message.content.lower()

    try:
        global voice, player

        # Bot owner / admin commands
        if message_content_lower.startswith("!ping") and user in var.owner_approved:
            await client.send_message(message.channel, "pong")
            print("Ping from server: {}".format(user_server))

        elif message_content_lower.startswith("!listservers") and user in var.owner_approved:
            servers = [server.name for server in client.servers]
            await client.send_message(message.channel, ", ".join(servers))
            print("listservers from server: {}".format(user_server))

        # Other commands
        elif message_content_lower.startswith("!coinflip"):
            flip = random.randint(1, 2)
            if flip == 1:
                await client.send_message(message.channel, "Heads wins :ok_hand:")
            else:
                await client.send_message(message.channel, "Tails wins :ok_hand:")

        elif message_content_lower.startswith("!roll"):
            die = random.randint(1, 6)
            await client.send_message(message.channel, "{} rolled {}".format(user, die))

        elif message_content_lower.startswith("!choice "):
            choices_str = message.content.split(" ", 1)[1]
            choices = choices_str.split(",")
            choice = random.randint(0, len(choices)-1)
            await client.send_message(message.channel, "I choose: {}".format(choices[choice]))

        elif message_content_lower.startswith("!yn "):
            yn = random.randint(1, 2)
            if yn == 1:
                await client.send_message(message.channel, "Yes")
            else:
                await client.send_message(message.channel, "No")

        elif message_content_lower.startswith("!numgen "):
            ran_str = message.content.split(" ", 1)[1]
            num1 = ran_str.split(",")[0]
            num2 = ran_str.split(",")[1]
            try:
                die = random.randint(int(num1), int(num2))
                await client.send_message(message.channel, "{} rolled {}".format(user, die))
            except (ValueError, TypeError):
                await client.send_message(message.channel, "Invalid number(s)")

        elif message_content_lower.startswith("!quote"):
            choice = random.randint(0, len(quotes)-1)
            await client.send_message(message.channel, quotes[choice])

        elif message_content_lower.startswith("!insult "):
            choice = random.randint(0, len(insults)-1)
            user = message.content.split(" ", 1)[1]
            insult_text = "{}{}".format(user, insults[choice])
            await client.send_message(message.channel, insult_text)

        elif message_content_lower.startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message_content_lower.startswith("!wiki "):
            search_req = message.content.split(" ", 1)[1]
            wiki_to_send = await misc_functions.search_wiki(search_req)
            await client.send_message(message.channel, wiki_to_send)

        elif message_content_lower.startswith("!define "):
            word = message.content.split(" ", 1)[1]
            defined_to_send = await misc_functions.get_definition(word)
            await client.send_message(message.channel, defined_to_send[:2000])

        elif message_content_lower.startswith("!ph "):
            search = message.content.split(" ", 1)[1]
            ph_to_send = await misc_functions.dirty_stuff(search)
            await client.send_message(message.channel, ph_to_send)

        elif message_content_lower.startswith("!urban "):
            ud_word = message.content.split(" ", 1)[1]
            ud_to_send = await misc_functions.get_urban_def(ud_word)
            await client.send_message(message.channel, ud_to_send[:2000])

        elif message_content_lower.startswith("!neo"):
            nasa_to_send = await misc_functions.get_NEOs()
            await client.send_message(message.channel, nasa_to_send)

        elif message_content_lower.startswith("!big "):
            words_to_big = message.content.split(" ", 1)[1]
            bigger_words = await misc_functions.big(" ".join(words_to_big))
            big_to_send = "".join(bigger_words)
            await client.send_message(message.channel, big_to_send)

        elif message_content_lower.startswith("!lads"):
            await client.send_message(message.channel, var.lads_text)

        elif message_content_lower.startswith("!holdon"):
            with open("Images/holdon.png", "rb") as sendfile:
                await client.send_file(message.channel, sendfile)

        elif message_content_lower.startswith("!roasted"):
            with open("Images/roastcard.jpg", "rb") as sendfile:
                await client.send_file(message.channel, sendfile)

        elif message_content_lower.startswith("!info"):
            await client.send_message(message.channel, var.info_text)

        elif message_content_lower.startswith("!help"):
            await client.send_message(message.channel, var.help_message)

        # - - - Voice stuff - - - #

        # TODO: Make !join and !waiting join different channel if called by user
        # in different channel

        elif message_content_lower.startswith("!waiting"):
            if user_voice_channel != None:
                try:
                    voice = await client.join_voice_channel(user_voice_channel)
                except discord.errors.ClientException:
                    pass  # Already in session
                try:
                    player.stop()
                except NameError:
                    pass  # Nothing playing
                player = voice.create_ffmpeg_player("Sounds/Elevator_Music.mp3")
                player.start()

        elif message_content_lower.startswith("!join"):
            if user_voice_channel != None:
                await client.send_message(message.channel, "Joining...")
                print("From user {}:\nRequest to join {}".format(user, user_voice_channel))

                try:
                    await voice.disconnect()
                except NameError:
                    pass  # Not connected

                try:
                    voice = await client.join_voice_channel(user_voice_channel)
                except discord.errors.ClientException:
                    await client.send_message(message.channel, "Cannot connect to voice channel")

        elif message_content_lower.startswith("!leave"):
            try:
                await voice.disconnect()
            except NameError:
                pass  # Not connected

        elif message_content_lower.startswith("!play "):
            if user_voice_channel != None and client.is_voice_connected(user_server):
                youtube_url = message.content.split(" ", 1)[1]
                print("From user {}:\nRequest to play: {}".format(user, youtube_url))

                try:
                    player.stop()
                except NameError:
                    pass  # Nothing playing

                await client.send_message(message.channel, "Playing `{}`...".format(youtube_url))

                try:
                    player = await voice.create_ytdl_player(youtube_url)
                    player.start()
                except youtube_dl.utils.DownloadError:
                    await client.send_message(message.channel, "Not a valid URL")

        elif message_content_lower.startswith("!stop"):
            try:
                player.stop()
            except NameError:  # Nothing playing
                pass

    except concurrent.futures._base.TimeoutError:
        print("concurrent.futures._base.TimeoutError occured")
        await client.send_message(message.channel, "Request timed out :cry:")

    except (ValueError, IndexError, NameError, TypeError):
        print("Something went wrong :(")
        await client.send_message(message.channel, "Something went wrong :cry:")

@client.event
async def on_ready():
    timestamp = dt.now().strftime("%H:%M")
    print("@ {}".format(timestamp))
    print("Logged in as\nUsername: {}\nID: {}".format(client.user.name, client.user.id))
    print("Playing with Rick <3\n------")
    await client.change_presence(game=discord.Game(name="with Rick <3"))

client.run(var.discord_token)
