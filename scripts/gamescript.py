import requests
import time
from utilities import *
from functools import reduce

def run_game_script(mode, tier_accepted, excluded_tournaments, url_name, folder_name, debug = False):
    headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"} # User-Agent for wikiapi
    tournaments = [] # List of all tournaments name
    tournaments_data = [] # List of all tournaments data
    players_data = [] # List of all players data
    print("Starting script for " + url_name + "...")

    # Get all tournaments
    for tier in tier_accepted:
        # Get tournaments list from the tier
        if debug:print("Getting " + tier + " tournaments list...")
        response = requests.get(f'https://liquipedia.net/{url_name}/api.php?action=parse&page={tier}_Tournaments&format=json', headers=headers)
        data = response.json()

        # Get all tournaments name
        presize = len(tournaments)
        tournaments += get_tournaments_name(data)
        if debug:print(f"## Found {len(tournaments) - presize} tournaments ! ##")

        # Prevent from being banned
        time.sleep(35)


    # Get all tournaments data
    n = 0
    minYear = 2100
    maxYear = 0
    for tournament in tournaments:
        n += 1
        if not debug: printProgressBar(n, len(tournaments), prefix = "Progress Tournaments:", suffix = "Complete")
        if tournament in excluded_tournaments:
            continue
        requestMade = False

        # Get tournament page data
        if debug: print(f"{n}/{len(tournaments)} : Getting {tournament} data...")
        data = None

        if mode == ParsingMode.NO_FETCHING or mode == ParsingMode.READ_FIRST_ALL:
            try:
                with open(f"results/{folder_name}/tournaments/"+tournament.replace('/', "-")+".json", "r") as input_file:
                    data = json.load(input_file)
            except:
                print("Tournament file not found: ", tournament)

        if data is None:
            if mode == ParsingMode.NO_FETCHING:
                if debug: print("No fetching, skipping tournament: ", tournament)
                continue
            response = requests.get(f'https://liquipedia.net/{url_name}/api.php?action=parse&page={tournament}&format=json', headers=headers)
            requestMade = True
            data = response.json()
            with open(f"results/{folder_name}/tournaments/"+tournament.replace('/', "-")+".json", "w") as output_file:
                json.dump(data, output_file)

        # Get tournament data
        tournament_data = get_tournament_data(data, folder_name, debug=debug)
        if tournament_data is not None:
            tournaments_data.append(tournament_data)
            year = get_tournament_start_year(tournament_data["start-date"])
            if year is not None:
                minYear = min(minYear, year)
                maxYear = max(maxYear, year)

        # Prevent from being banned
        if requestMade:
            time.sleep(35)


    # Get all players
    n = 0
    total_player_with_duplicates = len(reduce(lambda a1,a2 : a1 + a2, map(lambda tournament_data : tournament_data['players'], tournaments_data)))
    player_parsed = set()
    for tournament in tournaments_data:
        tournament_players = []
        for player in tournament['players']:
            n += 1
            if not debug:printProgressBar(n, total_player_with_duplicates, prefix = "Progress Players:    ", suffix = "Complete")
            if player.startswith('index.php'):
                continue

            if player in player_parsed:
                tournament_players.append(player)
                continue

            # Get player page data
            if debug: print(f"{n}/{total_player_with_duplicates} :Getting {player} data...")
            data = get_player_json_from_name(player, url_name, folder_name, headers, mode, debug=debug)

            # Process player data page
            pdata = get_player_data(data, folder_name, headers, mode, url_name, [], debug=debug)
            if pdata is not None:
                # verify that the player name is not already in the list players_data
                if pdata['nickname'] not in map(lambda player_data : player_data['nickname'], players_data):
                    players_data.append(pdata)
                    tournament_players.append(pdata['nickname'])
                    player_parsed.add(pdata['nickname'])

        tournament['players'] = tournament_players


    print("\n")
    # Read previous data
    with open('results/data.json', 'r') as f:
        data = json.load(f)

    # Append new data
    for player in players_data:
        data[folder_name]["players"][player['nickname']] = player
    data[folder_name]["tournaments"] = tournaments_data
    data[folder_name]["time-range"] = str(minYear) + "-" + str(maxYear)

    # Write the updated values back to the same file
    with open('results/data.json', 'w') as f:
        json.dump(data, f)


def printProgressBar (iteration, total, prefix, suffix):
    length = 40
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = "\r")