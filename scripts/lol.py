import requests
import time
from utilities import *
from functools import reduce


def run_test():
    with open("results/lol/test-tournaments/LCS-2022-Spring.json", "r") as input_file:
        data = json.load(input_file)
    tournament_data = get_tournament_data(data, "lol")


def run_lol(mode):
    tier_accepted = ["S-Tier"] # List of all accepted tournament tier
    excluded_tournaments = ["All-Star/2013", "All-Star/2014", "All-Star/2015", "All-Star/2016", "All-Star/2017", "All-Star/2018",
                            "All-Star/2020", "Mid-Season Invitational/2020", "Rift Rivals/LCK-LPL-LMS-VCS/2019", "Rift Rivals/NA-EU/2019",
                            "Rift Rivals/LCK-LPL-LMS/2018", "Rift Rivals/LLN-CLS-CBLOL/2018", "Rift Rivals/NA-EU/2018", "Rift Rivals/LCL-TCL-VCS/2018",
                            "Rift Rivals/SEA-LJL-OPL/2018", "Rift Rivals/LCL-TCL/2017", "Rift Rivals/LCK-LPL-LMS/2017", "Rift Rivals/NA-EU/2017",
                            "Rift Rivals/LLN-CLS-CBLOL/2017", "Rift Rivals/GPL-LJL-OPL/2017"]
    headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"} # User-Agent for wikiapi
    tournaments = [] # List of all tournaments name
    tournaments_data = [] # List of all tournaments data
    players_data = [] # List of all players data

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
        time.sleep(31)


    # Get all tournaments data
    n = 0
    for tournament in tournaments:
        n += 1
        if tournament in excluded_tournaments:
            continue
        requestMade = False

        # Get tournament page data
        print(f"{n}/{len(tournaments)} : Getting {tournament} data...")
        data = None

        if mode == ParsingMode.NO_FETCHING or mode == ParsingMode.READ_FIRST_ALL:
            try:
                with open("results/lol/tournaments/"+tournament.replace('/', "-")+".json", "r") as input_file:
                    data = json.load(input_file)
            except:
                print("Tournament file not found: ", tournament)

        if data is None:
            if mode == ParsingMode.NO_FETCHING:
                print("No fetching, skipping tournament: ", tournament)
                continue
            response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={tournament}&format=json', headers=headers)
            requestMade = True
            data = response.json()
            with open("results/lol/tournaments/"+tournament.replace('/', "-")+".json", "w") as output_file:
                json.dump(data, output_file)

        # Get tournament data
        tournament_data = get_tournament_data(data, "lol")
        if tournament_data is not None:
            tournaments_data.append(tournament_data)

        # Prevent from being banned
        if requestMade:
            time.sleep(31)


    # Get all players
    n = 0
    all_players = set(reduce(lambda a1,a2 : a1 + a2, map(lambda tournament_data : tournament_data['players'], tournaments_data)))
    total_player = len(all_players)
    for player in all_players:
        n += 1
        if player.startswith('index.php'):
            continue
        requestMade = False

        # Get player page data
        print(f"{n}/{total_player} :Getting {player} data...")
        data = None

        if mode == ParsingMode.NO_FETCHING or ParsingMode.READ_FIRST_ALL:
            try:
                with open("results/lol/players/"+player.replace('/', "-")+".json", "r") as input_file:
                    data = json.load(input_file)
            except:
                print("Player file not found: ", player)

        if data is None:
            if mode == ParsingMode.NO_FETCHING:
                print("No fetching, skipping player: ", player)
                continue
            response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={player}&format=json', headers=headers)
            requestMade = True
            data = response.json()
            with open("results/lol/players/"+player.replace('/', "-")+".json", "w") as output_file:
                json.dump(data, output_file)

        # Get player data
        pdata = get_player_data(data, "lol")
        if pdata is not None:
            players_data.append(pdata)

        # Prevent from being banned
        if requestMade:
            time.sleep(31)


    # Read previous data
    with open('results/data.json', 'r') as f:
        data = json.load(f)

    # Append new data
    data['lol']["players"] = players_data
    data['lol']["tournaments"] = tournaments_data

    # Write the updated values back to the same file
    with open('results/data.json', 'w') as f:
        json.dump(data, f)


#run_test()