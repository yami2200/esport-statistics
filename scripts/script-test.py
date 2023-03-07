import requests
import json

#response = requests.get('https://liquipedia.net/leagueoflegends/api.php?action=query&titles=Faker&prop=revisions&rvprop=content&format=json')
response = requests.get('https://liquipedia.net/rocketleague/api.php?action=query&titles=Vatira&prop=revisions&rvprop=content&format=json')
data = response.json()

with open("results/output-test-vatira.json", "w") as output_file:
    json.dump(data, output_file)