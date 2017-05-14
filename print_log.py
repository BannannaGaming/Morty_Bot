try:
    with open("Morty-bot.log", "r") as f:
        print(f.read())
except (FileNotFoundError, IOError):
    print("Cannot open file")
