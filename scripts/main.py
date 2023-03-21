from lol import *
from cs import *
from utilities import *

#######   Configuration   #######
mode = ParsingMode.READ_FIRST_ALL
games = ["rl", "cs"]

#######   Main   #######
print("Starting collecting data")
for game in games:
    if game == "lol": run_lol(mode)
    elif game == "rl": print("Rocket League is not supported yet")
    elif game == "cs": run_cs(mode)