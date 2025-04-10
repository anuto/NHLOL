from db.mongo_wrapper import *

def get_goal_info(goal, game_id, rosters_table, goals_table):
	scorer_id = goal['scoringPlayerId']
	scoring_player_search = rosters_table.find({'gameId': game_id, 'playerId': scorer_id})
	scoring_player = scoring_player_search.to_list()

	if not scoring_player or len(scoring_player) > 1:
		raise Exception("multiple records found for game " + game_id + ", player: " + scorer_id)

	scoring_player = scoring_player[0]

	goal_info = {}

	goal_info['scoringTeamId'] = scoring_player['teamId']
	goal_info['scoringPlayerId'] = scorer_id
	goal_info['goalieId'] = goal['goalieId']
	
	goal_info['gameId'] = game_id
	
	goal_info['timeInPeriod'] = goal['timeInPeriod']
	goal_info['periodNumber'] = goal['periodNumber']

	if 'videoUrl' in goal:
		goal_info['videoUrl'] = goal['videoUrl']
		
	goal_info['_id'] = goal['_id']

	return goal_info

def process_game(game, rosters_table, goals_table, multigoals):

	game_id = game['_id']

	print("getting goals for game..." + str(game_id))
	goals_cursor = goals_table.find({'gameId': game_id}	)

	prev_scoring_team = None
	combo = []

	for goal in goals_cursor:
		goal_info = get_goal_info(goal, game_id, rosters_table, goals_table)
		scoring_team = goal_info['scoringTeamId']

		if not prev_scoring_team or scoring_team == prev_scoring_team:
			combo.append(goal_info)

		else:
			if len(combo) > 1:
				multigoals.append({'gameId': game_id, 'combo': combo})

			combo = [goal_info]

		prev_scoring_team = scoring_team

	if len(combo) > 1:
		multigoals.append({'gameId': game_id, 'combo': combo})

def process_games(games_cursor):
	print("getting rosters...")
	rosters_table = get_raw_collection('rosters')

	print("getting goals...")
	goals_table = get_raw_collection('goals')

	game_num = 1

	multigoals = []

	for game in games_cursor:
		print("processing game " + str(game_num))
		game_num += 1
		
		process_game(game, rosters_table, goals_table, multigoals)

		print()
	return multigoals

	# not the greatest, but there's no good way to validate. no unique keys
	# since we've chosen to aggregate the multigoals.

def backfill_multigoals():
	print("getting games...")
	games_cursor = get_collection('games', {'gameType': 2})
	multigoals = process_games(games_cursor)
	rewrite_collection('multigoals', multigoals)

