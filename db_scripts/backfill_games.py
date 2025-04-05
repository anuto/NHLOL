from API_CONSTANTS import *
from db.mongo_wrapper import *
import requests

def get_team_schedule_url(team_abbrev):
	return API_BASE + "club-schedule-season/" + team_abbrev + "/" + SEASON

def copy_field(new_struct, old_struct, field):
	new_struct[field] = old_struct[field]

def copy_team_info(game, team_info, team_side):
	game[team_side + 'Id'] = team_info['id']
	game[team_side + 'CommonId'] = team_info['commonName']['default']
	game[team_side + 'PlaceName'] = team_info['placeName']['default']
	game[team_side + 'Abbrev'] = team_info['abbrev']
	game[team_side + 'Logo'] = team_info['logo']
	game[team_side + 'DarkLogo'] = team_info['darkLogo']

def process_games_for_team(team_abbrev, team_games):

	print("pulling games for " + team_abbrev + "...")
	url = get_team_schedule_url(team_abbrev)

	team_schedule_response = requests.get(url)
	team_schedule_data = team_schedule_response.json()
	team_games_data = team_schedule_data['games']

	for game_data in team_games_data:
		game_id = game_data['id']

		if game_data['id'] not in team_games:
			game = {}

			game['_id'] = game_id
			copy_field(game, game_data, 'gameType')
			copy_field(game, game_data, 'gameDate')

			away_team = game_data['awayTeam']
			home_team = game_data['homeTeam']

			copy_team_info(game, away_team, "awayTeam")
			copy_team_info(game, home_team, "homeTeam")

			print(game)

			team_games[game_id] = game

# process_games_for_team("SEA")

teams_cursor = get_collection('teams')
team_games = {}

for team in teams_cursor:
	team_abbrev = team['abbrev']
	url = get_team_schedule_url(team_abbrev)
	process_games_for_team(team_abbrev, team_games)

update_collection_with_dictionary('games', team_games)
