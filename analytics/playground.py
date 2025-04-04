from db.mongo_wrapper import *

# goals = get_collection('goals').to_list()
# num_goals = len(goals)
# print("all goals: " + str(num_goals))

# specific_goals = get_collection('goals', {'gameId': 2024010015}).to_list()
# num_specific_goals = len(specific_goals)
# print("2024010015 goals: " + str(num_specific_goals))

print("getting games...")
games_cursor = get_collection('games', {'gameType': 2})

print("getting rosters...")
rosters_table = get_raw_collection('rosters')

multikills = {}

game_num = 1

for game in games_cursor:
	print("processing game " + str(game_num))
	game_num += 1

	game_id = game['_id']

# game_id = 2024010015

	print("getting goals...")
	goals_cursor = get_collection('goals', {'gameId': game_id})

	prev_scoring_team = None
	prev_period = -1

	combo = 0
	goal_num = 1

	for goal in goals_cursor:
		# print("processing goal " + str(goal_num))
		goal_num += 1

		period = goal['periodNumber']
		print("[period " + str(period) + "] " + goal['timeInPeriod'])

		scorer_id = goal['scoringPlayerId']
		scoring_player_search = rosters_table.find({'gameId': game_id, 'playerId': scorer_id})
		scoring_player = scoring_player_search.to_list()

		if not scoring_player or len(scoring_player) > 1:
			raise Exception("multiple records found for game " + game_id + ", player: " + scorer_id)

		scoring_player = scoring_player[0]
		scoring_team = scoring_player['teamId']

		combo += 1

		if prev_scoring_team and scoring_team == prev_scoring_team:
			if period == prev_period:
				if combo not in multikills:
					multikills[combo] = []

				multikills[combo].append(goal)
			else:
				combo = 1
		else:
			combo = 1

		prev_scoring_team = scoring_team
		prev_period = period

	print()

print(multikills)


