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

# interestingly, at this level kraken are amongst the best. but not by 
# a significant amount.

# examine_doubles(120)

# tied for best at this point. but everyone is 1-6 range, so.

# examine_doubles(60)

# kraken still huge here

# examine_doubles(30)

# only 4 teams - MTL, WSH, SEA, and VAN. All one each.
games = examine_doubles(10)
