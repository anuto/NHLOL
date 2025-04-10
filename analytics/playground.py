from process_multigoals import *
import collections
from db.mongo_wrapper import *

# HAHAHA RIP KRAKEN 2024020684
# BUT RIP SID CROSBY MORE 2024021131
def examine_quadras(time_limit):
	combos = process_multigoals_by_period_with_time_limit(time_limit)

	print()
	quadras = combos[4]

	for quadra in quadras:
		game = quadra[0]
		game_id = game['gameId']
		print(str(game_id))


# two and only two back to back goals
def examine_doubles(time_limit):
	combos = process_multigoals_by_period_with_time_limit(time_limit)

	doubles = combos[2]

	team_games = {}
	scoring = []

	# this doesn't include triples and quadras and such though...
	for double in doubles:
		game = double[0]
		scoring_team_id = game['scoringTeamId']
		scoring.append(scoring_team_id)

		if scoring_team_id not in team_games:
			team_games[scoring_team_id] = []

		team_games[scoring_team_id].append(double)

	team_counter_by_id = collections.Counter(scoring)

	teams_table = get_raw_collection("teams")

	team_counter = {}

	for team_id in team_counter_by_id:
		team = teams_table.find({'_id': team_id}).to_list()[0]
		team_name = team['abbrev']
		team_counter[team_name] = team_counter_by_id[team_id]

		team_games[team_name] = team_games.pop(team_id)

	team_counter = collections.Counter(team_counter)

	print(team_counter.most_common())
	return team_games

def process_double(combo, scoring, team_games):
	game = combo[0]
	scoring_team_id = game['scoringTeamId']
	scoring.append(scoring_team_id)

	if scoring_team_id not in team_games:
		team_games[scoring_team_id] = []

	team_games[scoring_team_id].append(combo)

# all back to back goals (even in a chain of more goals)
def examine_all_doubles(time_limit):
	combos = process_multigoals_by_period_with_time_limit(time_limit)

	combos_lengths = combos.keys()

	team_games = {}
	scoring = []

	for combo_length in combos_lengths:
		combos_of_length = combos[combo_length]

		if combo_length == 2:
			for double in combos_of_length:
				process_double(double, scoring, team_games)
		else:
			for combo_of_length in combos_of_length:
				doubles = []
				prev_goal = combo_of_length[0]

				# split all combos longer than 2 into back to back
				# goals. ex. [goalA, goalB, goalC] => 
				# [[goalA, goalB], [goalB, goalC]]
				for combo_index in range(1, combo_length):
					next_goal = combo_of_length[combo_index]
					doubles.append([prev_goal, next_goal])
					prev_goal = next_goal

				for double in doubles:
					process_double(double, scoring, team_games)

	team_counter_by_id = collections.Counter(scoring)

	teams_table = get_raw_collection("teams")

	team_counter = {}

	for team_id in team_counter_by_id:
		team = teams_table.find({'_id': team_id}).to_list()[0]
		team_name = team['abbrev']
		team_counter[team_name] = team_counter_by_id[team_id]

		team_games[team_name] = team_games.pop(team_id)

	team_counter = collections.Counter(team_counter)

	print(team_counter.most_common())
	return team_games

# interestingly, at this level kraken are amongst the best. but not by 
# a significant amount.

# examine_doubles(120)
# examine_all_doubles(120)

# examine_doubles(60)
# examine_all_doubles(60)

# kraken tied for first in both. basically the same here

# examine_doubles(30)
# examine_all_doubles(30)

# only 4 teams - MTL, WSH, SEA, and VAN. All one each.
# games = examine_doubles(10)
# games = examine_all_doubles(10)

games = process_all_multigoals()
# print(collections.Counter(games))