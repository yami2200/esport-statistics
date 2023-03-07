import requests
import json
from bs4 import BeautifulSoup

tier_accepted = ["S-Tier"]
headers = {'User-Agent': "Open Source E-Sport Data Engineering School Project"}

# Get all tournaments
for tier in tier_accepted:
    response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page={tier}_Tournaments&format=json', headers=headers)
    data = response.json()

    with open("results/lol/tournaments-" + tier + ".json", "w") as output_file:
        json.dump(data, output_file)


# response = requests.get(f'https://liquipedia.net/leagueoflegends/api.php?action=parse&page=LPL/2022/Spring&format=json', headers=headers)

def get_tournament_data(json_data):
    html = json_data['parse']['text']['*']