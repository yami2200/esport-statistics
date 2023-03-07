import requests
import json

response = requests.get('https://liquipedia.net/leagueoflegends/api.php?action=query&titles=World_Championship/2022&prop=revisions&rvprop=content&format=json')
#response = requests.get('https://liquipedia.net/rocketleague/api.php?action=query&titles=Vatira&prop=revisions&rvprop=content&format=json')
data = response.json()

with open("results/output-test-world.json", "w") as output_file:
    json.dump(data, output_file)