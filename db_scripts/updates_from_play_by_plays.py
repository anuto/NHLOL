from API_CONSTANTS import *
from db.mongo_wrapper import *
import requests
import warnings

UPDATE_GOALS = False
UPDATE_GAMES = False
UPDATE_ROSTERS = True

# this follows the 'update_' paradigm, but it takes some time to run and the prior data
# probably won't change unless there is a backfill. shrug.

def copy_field(new_struct, old_struct, field):
	if field in old_struct:
		new_struct[field] = old_struct[field]
	else:
		new_struct[field] = None

def copy_default_value(new_struct, old_struct, field):
	if field in old_struct:
		new_struct[field] = old_struct[field]['default']
	else:
		new_struct[field] = None

def get_play_by_play_url(game_id):
	return API_BASE + "gamecenter/" + str(game_id) + "/play-by-play"

def process_play_by_plays(pbp_data):
	game_id = pbp_data['id']

	goals = []

	plays_data = pbp_data['plays']

	print("number plays: " + str(len(plays_data)))
	i = -1

	for play_data in plays_data:
		i+=1
		event_desc = play_data['typeDescKey']

		if event_desc == 'goal':

			goal = {}

			goal['gameId'] = game_id

			copy_field(goal, play_data, 'eventId')
			copy_field(goal, play_data, 'timeInPeriod')
			copy_field(goal, play_data, 'timeRemaining')
			copy_field(goal, play_data, 'typeCode')
			copy_field(goal, play_data, 'typeDescKey')

			copy_field(goal, play_data['details'], 'zoneCode')
			copy_field(goal, play_data['details'], 'shotType')
			copy_field(goal, play_data['details'], 'scoringPlayerId')

			period_number = play_data['periodDescriptor']['number']
			goal['periodNumber'] = period_number

			# sigh...some are just missing them randomly.
			if 'highlightClipSharingUrl' in play_data['details'] and period_number < 4:
				copy_field(goal, play_data['details'], 'highlightClipSharingUrl')

			elif 'highlightClipSharingUrlFr' in play_data['details'] and period_number < 4:
				goal['highlightClipSharingUrl'] = play_data['details']['highlightClipSharingUrlFr']

			elif period_number < 4:
				warnings.warn("no replay for goal event " + str(play_data['eventId']) + " at idx " + str(i))
				goal['highlightClipSharingUrl'] = None

			goals.append(goal)

	print("number goals: " + str(len(goals)))
	print("adding plays to db...")
	update_goals_collection('goals', goals)
	print("done!")

def process_expanded_game_info(pbp_data):
	game_extra_data = {}

	game_extra_data['venue'] = pbp_data['venue']['default']

	if 'venueLocation' in pbp_data:
		venueLocation = pbp_data['venueLocation']

		if 'default' in venueLocation:
			game_extra_data['venueLocation'] = venueLocation['default']
		elif 'fr' in venueLocation:
			game_extra_data['venueLocation'] = venueLocation['fr']
		else:
			game_extra_data['venueLocation'] = None

	# isn't for future games
	if 'periodDescriptor' in pbp_data:
		game_extra_data['numberPeriods'] = pbp_data['periodDescriptor']['number']
	else:
		game_extra_data['numberPeriods'] = None

	print(game_extra_data)
	return game_extra_data

# player_id is not unique nor will it always line up with the same team, even across a single 
# season due to trades. I need a mapping of
# (game_id, player_id) => which team?
def process_pbp_roster_for_game(pbp_data, game_id):
	roster = []

	roster_data = pbp_data['rosterSpots']

	for player_data in roster_data:
		player = {}

		player['gameId'] = game_id

		copy_field(player, player_data, 'teamId')
		copy_field(player, player_data, 'playerId')
		copy_field(player, player_data, 'sweaterNumber')
		copy_field(player, player_data, 'positionCode')
		copy_field(player, player_data, 'headshot')

		copy_default_value(player, player_data, 'firstName')
		copy_default_value(player, player_data, 'lastName')

		roster.append(player)

	return roster

games_cursor = get_collection('games')
game_number = 1

games_expanded_data = {}

for game in games_cursor:
	print("processing game " + str(game_number))
	game_number += 1

	game_id = game['_id']
	play_by_play_url = get_play_by_play_url(game_id)
	print(play_by_play_url)

	pbp_response = requests.get(play_by_play_url)
	pbp_data = pbp_response.json()

	if UPDATE_GOALS:
		process_play_by_plays(pbp_data)

	if UPDATE_GAMES:
		game_expanded_data = process_expanded_game_info(pbp_data)

		print("updating game " + str(game_id) + " in db...")
		add_fields_to_document_in_collection('games', game_id, game_expanded_data)
		print("done!")

	if UPDATE_ROSTERS:
		print("updating roster for game " + str(game_id) + " in db...")
		game_roster = process_pbp_roster_for_game(pbp_data, game_id)
		update_players_collection('rosters', game_roster)
		print("done!")

	print()
