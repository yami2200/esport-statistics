from lol import *
from utilities import *

#######   Configuration   #######
mode = ParsingMode.NO_FETCHING
games = ["lol", "rl", "cs"]

#######   Main   #######
print("Starting collecting data")
for game in games:
    if game == "lol": run_lol(mode)
    elif game == "rl": print("Rocket League is not supported yet")
    elif game == "cs": print("Counter Strike is not supported yet")