"""
var.py

variables which will be unchanged during runtime and
are used in replies / data requests
"""

from platform import python_version
import platform
import os

owner_approved = ["<@263412940869206027>"]

youtube_playlist = []

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

• **Memes**
  • `!holdon`
    • Bitch, hold on
  • `!roasted`
    • `https://youtu.be/_tWC5qtfby4`
  • `!lads`
    • Banter

• **Information**
  • `!neo`
    • Get the closest near earth object (uses NASA API)

• **Music/Sounds**
  • ***note***: playlist not automatic yet, `!playnext` must be called after a song finishes
  • `!join`
    • Joins the voice channel you are in
  • `!leave`
    • Leaves whatever channel it is in
  • `!playnext`
    • Start playing playlist / skip to next song [CRASHES OCCASIONALLY]
  • `!stop`
    • Stop playing audio
  • `!add` `youtube url`
    • Add a youtube url to the playlist [playlist erased occasionally]
  • `!playlist`
    • Show what is currently in the playlist
  • `!chill`
    • Add some randomally chosen background music to the playlist
  • `!waiting`
    • Add some music for waiting to the playlist 

• **Random Selection**
  • `!coinflip`
    • Heads or tails!
  • `!roll`
    • Returns a random number between 1 & 6
  • `!numgen` `num1,num2`
    • Returns a random number between num1 & num2
  • `!yn`
    • Returns `Yes` or `No`
  • `!choice` `Comma,Seperated,List,Of,Choices`
    • Pick a value from a given list of choices

• **Misc**
  • `!quote`
    • Get a random Rick and Morty quote
  • `!big` `text to make bigger`
    • Make text bigger
  • `!insult` `name`
    • Insult someone
  • `!info`
    • Get information about this bot
  • `!help`
    • Shows this menu

• **Bot Owner**
  • `!ping`
  • `!listservers`

• ***COMING SOON***
  • `!youtube` `search term`
  • `!imgur` `search term`
  • Completely replacing mee6 (fuck that guy)
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
Platform       : {}
- - - -  --  - - - -
```
Test me on my own server : https://www.discord.gg/kDE7HJy
My source code : https://github.com/thatguywiththatname/Morty_Bot
""".format(python_version(),
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
NEO_text = """
**Near Earth Object - Name: {}**
```Estimated diameter          | {} meters
Potentially hazardous?      | {}
Close approach date         | {}
Velocity                    | {}mph
Distance from earth on miss | {} meters```"""

# Ladssss
lads_text = """
Look at these l a d s
<:simm:304715724193005568> <:sem:304711598793293825> <:ricc:304717179071234049> <:gman:304708365614055424> <:actuallyhitler:304719065799327744> <:cammW:304720572158443520>
"""

# https://gist.github.com/hzsweers/8595628
# Get env variable(s) from Heroku
discord_token = os.environ["morty_discord_token"]
yt_api_key    = os.environ["yt_key"]
nasa_api_key  = os.environ["nasa_key"]
