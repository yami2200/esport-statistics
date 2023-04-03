from lol import *
from cs import *
from rl import *
from utilities import *
import shutil
import os

# https://liquipedia.net/api-terms-of-use

#######   Configuration   #######
mode = ParsingMode.READ_FIRST_ALL
games = ["lol", "rl", "cs"]

#######   Main   #######
print("Starting collecting data")
for game in games:
    if game == "lol": run_lol(mode)
    elif game == "rl": run_rl(mode)
    elif game == "cs": run_cs(mode)

# Copy data.json to src/assets
cwd = os.getcwd()
src_file = os.path.join(cwd, "results", "data.json")
dst_file = os.path.abspath(os.path.join(cwd, os.pardir, "src", "assets", "data.json"))
shutil.copy(src_file, dst_file)