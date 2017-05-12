"""
This code sucks, you know it and I know it.
Async is hard...
Move on and call me an idiot later.
"""

from datetime import datetime as dt
import misc_functions
import discord
import random
import var

# Most send's have [:2000] to prevent going over message length limit

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

    try:
        # Bot owner / admin commands
        if message.content.lower().lower().startswith("!ping") and user in var.owner_approved:
            await client.send_message(message.channel, "pong")
            print("Ping from server: {}".format(message.server))

        elif message.content.lower().lower().startswith("!listservers") and user in var.owner_approved:
            servers = [server.name for server in client.servers]
            await client.send_message(message.channel, ", ".join(servers))
            print("listservers from server: {}".format(message.server))

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

        elif message.content.lower().startswith("!insult "):
            choice = random.randint(0, len(insults)-1)
            user = message.content.split(" ", 1)[1]
            insult_text = "{}{}".format(user, insults[choice])
            await client.send_message(message.channel, insult_text)

        elif message.content.lower().startswith("!kys"):
            await client.send_message(message.channel, "I agree, :regional_indicator_k: :regional_indicator_y: :regional_indicator_s:")

        elif message.content.lower().startswith("!wiki "):
            search_req = message.content.split(" ", 1)[1]
            wiki_to_send = await misc_functions.search_wiki(search_req)
            await client.send_message(message.channel, wiki_to_send)

        elif message.content.lower().startswith("!define "):
            word = message.content.split(" ", 1)[1]
            defined_to_send = await misc_functions.get_definition(word)
            await client.send_message(message.channel, defined_to_send[:2000])

        elif message.content.lower().startswith("!ph "):
            search = message.content.split(" ", 1)[1]
            ph_to_send = await misc_functions.dirty_stuff(search)
            await client.send_message(message.channel, ph_to_send)

        elif message.content.lower().startswith("!urban "):
            ud_word = message.content.split(" ", 1)[1]
            ud_to_send = await misc_functions.get_urban_def(ud_word)
            await client.send_message(message.channel, ud_to_send[:2000])

        elif message.content.lower().startswith("!neo"):
            nasa_to_send = await misc_functions.get_NEOs()
            await client.send_message(message.channel, nasa_to_send)

        elif message.content.lower().startswith("!big "):
            words_to_big = message.content.split(" ", 1)[1]
            bigger_words = await misc_functions.big(" ".join(words_to_big))
            big_to_send = "".join(bigger_words)
            await client.send_message(message.channel, big_to_send)

        elif message.content.lower().startswith("!lads"):
            await client.send_message(message.channel, var.lads_text)

        elif message.content.lower().startswith("!holdon"):
            with open("Images/holdon.png", "rb") as sendfile:
                await client.send_file(message.channel, sendfile)

        elif message.content.lower().startswith("!roasted"):
            with open("Images/roastcard.jpg", "rb") as sendfile:
                await client.send_file(message.channel, sendfile)

        elif message.content.lower().startswith("!info"):
            await client.send_message(message.channel, var.info_text)

        elif message.content.lower().startswith("!help"):
            await client.send_message(message.channel, var.help_message)

        elif message.content.lower().startswith("!start"):
            test_url = "https://www.youtube.com/watch?v=LdPyYze2NIA"

            channel = client.get_channel("262355614523457537")
            voice = await client.join_voice_channel(channel)

            player = await voice.create_ytdl_player(test_url)
            player.start()

        elif message.content.lower().startswith("!stop"):
            player.stop()

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
