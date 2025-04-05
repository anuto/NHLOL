import mongo_wrapper
from API_CONSTANTS import *
import requests

teams_response = requests.get(TEAMS_URL)
teams_data = teams_response.json()['data']

teams = []

for team_data in teams_data:
	team = {}

	team['_id'] = team_data['id']
	team['franchiseId'] = team_data['franchiseId']
	team['fullName'] = team_data['fullName']
	team['abbrev'] = team_data['triCode']

	teams.append(team)

mongo_wrapper.update_collection('teams', teams)

