import time
from enum import Enum

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


class ParsingMode(Enum):
    NO_FETCHING = 1 # Parse all data
    READ_FIRST_ALL = 2 # Parse all data but fetch only the data that is not stored locally
    UPDATE = 3 # Parse all data but fetch only data from this year and last year
    ALL = 4 # Fetch all data


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


def get_tournament_data(json_data, game, debug=False):
    tournament = load_json_file("tournament.json")

    html = json_data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')

    try:
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
        tournament['prize-pool'] = string_price_pool_to_number(prizepool_text.split('$')[1])

        # Get Players
        participating_teams = soup.findAll('div', class_='teamcard-inner')
        for flag in participating_teams:
            players_list = flag.findAll('tr', {'class': None, 'id': None})
            for player in players_list:
                # Eliminate coachs and players who haven't played
                if player.find('abbr', {'title': ['Coach', 'Did not play']}) is None and player.find('img', {'alt': 'Head Coach'}) is None and player.find('b', class_='placement-text') is None:
                    player_name_and_flag = player.findAll('a')
                    # Eliminate Promotion and competition name
                    if player_name_and_flag != [] and player_name_and_flag[0].find('img'):
                        if player_name_and_flag[1] is not None:
                            player_name = player_name_and_flag[1]['href'].split('/')[2]
                            if not player_name.startswith('index.php'):
                                tournament['players'].append(player_name)

        # Get Teams
        teams_html = soup.find_all('div', class_='block-team')
        tournament['teams'] = set()
        for team in teams_html:
            teams_a = team.find('a')
            if teams_a is not None:
                tournament['teams'].add(teams_a.get('title'))
        tournament['teams'] = list(tournament['teams'])

        # Get Viewers
        try:
            peakViewers = soup.find('td', string=' Peak Viewers')
            peakViewers = peakViewers.find_next("td")
            tournament["peak-viewers"] = int(peakViewers.text.replace(' ', ''))
        except:
            tournament["peak-viewers"] = 0
        try:
            avgViewers = soup.find('td', string=' Average Viewers')
            avgViewers = avgViewers.find_next("td")
            tournament["average-viewers"] = int(avgViewers.text.replace(' ', ''))
        except:
            tournament["average-viewers"] = 0

        return tournament
    except:
        if debug:print("Error in tournament: ", tournament['name'])
        return None


def get_player_json_from_name(player, url_name, folder_name, headers, mode, oldnames=None, debug=False):
    if oldnames is not None:
        if player in oldnames:
            if debug: print("Player already fetched, recursive redirect page", player)
            return None


    data = None
    if mode == ParsingMode.NO_FETCHING or ParsingMode.READ_FIRST_ALL:
        if oldnames is None or player.lower() not in map(lambda n: n.lower(), oldnames):
            try:
                with open(f"results/{folder_name}/players/"+player.replace('/', "-")+".json", "r") as input_file:
                    data = json.load(input_file)
            except:
                if debug:print("Player file not found: ", player)

    if data is None:
        if mode == ParsingMode.NO_FETCHING:
            if debug:print("No fetching, skipping player: ", player)
            return None
        if debug:print("Fetching player from Liquipedia: ", player)
        response = requests.get(f'https://liquipedia.net/{url_name}/api.php?action=parse&page={player}&format=json', headers=headers)
        data = response.json()
        time.sleep(35)
        with open(f"results/{folder_name}/players/"+player.replace('/', "-")+".json", "w") as output_file:
            json.dump(data, output_file)

    if oldnames is not None:
        oldnames.append(player)
    return data


def get_player_data(json_data, game, headers, mode, url_name, oldnames=None, debug=False):
    player = load_json_file("player.json")
    if json_data is None:
        return None

    try:
        html = json_data['parse']['text']['*']
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as inst:
        if debug:print("Error in player parsing :")
        if debug:print("--->  " + str(type(inst)))
        if debug:print("--->  " + str(inst))
        if debug:print("--->  " + str(json_data))

        return None

    # Check if there is no multiple player with the same nickname
    ambiguous_name_list = soup.find_all('a', string=lambda t: t and "disambiguation page" in t)
    if len(ambiguous_name_list) > 0:
        if debug:print("Error : multiple player with the same name")
        return None

    # Check if it's not a redirect page
    redirect_text = soup.find('div', attrs={"class": "redirectMsg"})
    if redirect_text:
        name = redirect_text.find_next('a').text
        if oldnames is None:
            oldnames = []
        return get_player_data(get_player_json_from_name(name, url_name, game, headers, mode, oldnames, debug=debug), game, headers, mode, url_name, oldnames, debug=debug)


    # Get player name
    try:
        player["nickname"] = json_data['parse']['title']
        romanized_name_div = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Romanized Name:')
        if romanized_name_div is not None:
            name_text = romanized_name_div.find_next_sibling('div').text
            player['name'] = name_text
        else:
            name_div = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Name:')
            name_text = name_div.find_next_sibling('div').text
            player['name'] = name_text
    except:
        if debug:print("Error in player name")
        return None


    # Get player birthdate
    try:
        born = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Born:')
        born_text = born.find_next_sibling('div').text
        player['birthdate'] = format_date(born_text)
    except:
        player['birthdate'] = "unknown"

    # Get Player Country
    country = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Nationality:')
    country_text = country.find_next(lambda tag: tag.name == 'a' and tag.text).text
    player['country'] = country_text

    # Get player approx total winnings
    try:
        winning = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Approx. Total Winnings:')
        winning_text = winning.find_next_sibling('div').text
        player['approx-total-winning'] = string_price_to_number(winning_text)
    except:
        player['approx-total-winning'] = 0

    # Get player status
    try:
        status = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Status:')
        status_text = status.find_next_sibling('div').text
        player['status-active'] = status_text == "Active"
    except:
        try:
            status = soup.find('div', attrs={'class': 'infobox-cell-2 infobox-description'}, string='Years Active (Player):')
            status_text = status.find_next_sibling('div').text
            player['status-active'] = "Present" in status_text
        except:
            if debug:print("Error in player status")
            return None

    return player


def get_tournament_start_year(date):
    if date is None:
        return None
    try:
        year = int(date.split('/')[2])
    except:
        return None
    return year
