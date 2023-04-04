from utilities import *


def test():
    headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"} # User-Agent for wikiapi
    with open(f"results/lol/players/Insec.json", "r") as input_file:
        data = json.load(input_file)
    get_player_data(data, "lol", headers, ParsingMode.READ_FIRST_ALL, "leagueoflegends")


def test2():
    headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"}
    mode = ParsingMode.READ_FIRST_ALL
    print(get_player_data(get_player_json_from_name("DanDy", "leagueoflegends", "lol", headers, mode), "lol", headers, mode, "leagueoflegends", []))


def test3():
    headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"}
    response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page=InSec&format=json', headers=headers)
    data = response.json()
    time.sleep(35)
    print(data)


test2()