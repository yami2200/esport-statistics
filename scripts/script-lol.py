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


def transform_date(date_str):
    year, month, day = date_str.split('-')
    return f"{day}/{month}/{year}"


def string_price_to_number(s):
    return int(s.replace(',', '').replace('$', ''))


def string_price_pool_to_number(s):
    return int(s.replace(',', '').replace('$', '').split('\xa0')[0])


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
    tournament = load_json_file("tournament.json")

    html = json_data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')

    # Get tournament name
    tournament_name = soup.find('div', attrs={'class' : "infobox-header wiki-backgroundcolor-light"})
    tournament['name'] = tournament_name.text.replace(tournament_name.span.text, '').strip()

    # Get tournament date
    startdate = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Start Date:')
    startdate_text = startdate.find_next_sibling('div').text
    tournament['start-date'] = transform_date(startdate_text)
    enddate = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='End Date:')
    enddate_text = enddate.find_next_sibling('div').text
    tournament['end-date'] = transform_date(enddate_text)

    # Get tournament Location
    location = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Location:')
    tournament['location'] = location.find_next('a')['title']

    # Get Team Winner
    team_winner = soup.find('span', attrs={'title' : "First"})
    tournament['team-winner'] = team_winner.find_next('div', attrs={'class': 'block-team'}).find_next('a')['title']

    # Get Prize Pool
    prizepool = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Prize Pool:')
    prizepool_text = prizepool.find_next_sibling('div').text
    tournament['prize-pool'] = string_price_pool_to_number(prizepool_text)

    # Get Players
    with_tag_lol = soup.find('span', id='Country_Representation')
    siblings = with_tag_lol.find_all_next('div', class_='table-responsive')
    siblings_soup = siblings[0]
    players_markup = siblings_soup.find_all('a')
    for p in players_markup:
        if p.text != "":
            tournament['players'].append(p.text)

    # Get Teams
    teams_html = soup.find_all('div', class_='block-team')
    tournament['teams'] = set()
    for team in teams_html:
        teams_a = team.find('a')
        if teams_a is not None:
            tournament['teams'].add(teams_a.get('title'))

    return tournament


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