import requests
import json
from bs4 import BeautifulSoup
import time

tier_accepted = ["S-Tier"] # List of all accepted tournament tier
headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"} # User-Agent for wikiapi
tournaments = [] # List of all tournaments name
tournaments_data = [] # List of all tournaments data
players_data = [] # List of all players data


def is_tournament_list(obj):
    return obj["ns"] == 0 and obj["*"].find("/") > 0


def get_tournament_name(obj):
    return obj["*"]


def get_tournaments_name(json_data):
    return map(get_tournament_name, filter(is_tournament_list, json_data['parse']['links']))


def get_tournament_data(json_data):
    html = json_data['parse']['text']['*']


def get_player_data(json_data):
    html = json_data['parse']['text']['*']


def players_already_exist(playername):
    return len(filter(lambda p: p["name"] == playername, players_data)) > 0


# Get all tournaments
for tier in tier_accepted:
    # Get tournaments list from the tier
    print("Getting " + tier + " tournaments list...")
    response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={tier}_Tournaments&format=json', headers=headers)
    data = response.json()

    # Get all tournaments name
    presize = len(tournaments)
    tournaments += get_tournaments_name(data)
    print(f"## Found {len(tournaments) - presize} tournaments ! ##")

    # Prevent from being banned
    time.sleep(2.1)


# Get all tournaments data
n = 1
for tournament in tournaments:
    # Get tournament page data
    print(f"{n}/{len(tournaments)} : Getting {tournament} data...")
    response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={tournament}&format=json', headers=headers)
    data = response.json()

    # Get tournament data
    tournaments_data.append(get_tournament_data(data))
    n += 1

    # Prevent from being banned
    time.sleep(2.1)


# Get all players
for tournament in tournaments_data:
    for player in tournament['players']:
        if players_already_exist(player):
            continue

        # Get player page data
        print(f"Getting {player} data...")
        response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={player}&format=json', headers=headers)
        data = response.json()

        # Get player data
        players_data.append(get_player_data(data))

        # Prevent from being banned
        time.sleep(2.1)


# Read previous data
with open('results/data.json', 'r') as f:
    data = json.load(f)

# Append new data
data['lol']["players"] = players_data
data['lol']["tournaments"] = tournaments_data

# Write the updated values back to the same file
with open('results/data.json', 'w') as f:
    json.dump(data, f)