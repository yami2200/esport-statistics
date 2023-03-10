import requests
import json
from bs4 import BeautifulSoup
import time
import sys
from datetime import datetime

tier_accepted = ["S-Tier"] # List of all accepted tournament tier
headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"} # User-Agent for wikiapi
tournaments = [] # List of all tournaments name
tournaments_data = [] # List of all tournaments data
players_data = [] # List of all players data


def format_date(date_str):
    newdate_str = date_str.split('(')[0].strip()
    date = datetime.strptime(newdate_str, '%B %d, %Y')
    formatted_date = date.strftime('%d/%m/%Y')
    return formatted_date


def string_price_to_number(s):
    return int(s.replace(',', '').replace('$', ''))


def is_tournament_list(obj):
    return obj["ns"] == 0 and obj["*"].find("/") > 0


def get_tournament_name(obj):
    return obj["*"]


def get_tournaments_name(json_data):
    return map(get_tournament_name, filter(is_tournament_list, json_data['parse']['links']))


def load_json_file(filename):
    with open("data-structure/"+filename, 'r') as f:
        return json.load(f)


def get_tournament_data(json_data):
    html = json_data['parse']['text']['*']


def get_player_data(json_data):
    player = load_json_file("player.json")

    html = json_data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')

    # Get player name
    romanized_name_div = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Romanized Name:')
    if romanized_name_div is not None:
        name_text = romanized_name_div.find_next_sibling('div').text
        player['name'] = name_text
    else:
        name_div = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Name:')
        name_text = name_div.find_next_sibling('div').text
        player['name'] = name_text

    # Get player birthdate
    born = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Born:')
    born_text = born.find_next_sibling('div').text
    player['birthdate'] = format_date(born_text)

    # Get Player Country
    country = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Nationality:')
    country_text = country.find_next(lambda tag: tag.name == 'a' and tag.text).text
    player['country'] = country_text

    # Get player approx total winnings
    winning = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Approx. Total Winnings:')
    winning_text = winning.find_next_sibling('div').text
    player['approx-total-winning'] = string_price_to_number(winning_text)

    # Get player status
    status = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Status:')
    status_text = status.find_next_sibling('div').text
    player['status-active'] = status_text == "Active"

    return player


def players_already_exist(playername):
    return len(filter(lambda p: p["name"] == playername, players_data)) > 0


response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page=Faker&format=json', headers=headers)
data = response.json()

get_player_data(data)

sys.exit(0)


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