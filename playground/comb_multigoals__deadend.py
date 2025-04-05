from db.mongo_wrapper import *

print("getting multigoals...")
multigoals = get_collection('multigoals')

print("getting rosters...")
rosters_table = get_raw_collection('rosters')

multigoals_combed = []

goal_num = 1

for goal in multigoals:
	print("processing goal " + str(goal_num))
	goal_num += 1

	goal_info = {}

	goal_info['_id'] = goal['_id']
	goal_info['timeInPeriod'] = goal['timeInPeriod']
	goal_info['zoneCode'] = goal['zoneCode']
	goal_info['periodNumber'] = goal['periodNumber']

	gameId = goal['gameId']
	goal_info['gameId'] = gameId

	scoringPlayerId = goal['scoringPlayerId']
	goal_info['scoringPlayerId'] = scoringPlayerId

	scoring_player_query = rosters_table.find({
		'playerId': scoringPlayerId,
		'gameId': gameId
	}).to_list()

	if not scoring_player_query or len(scoring_player_query) != 1:
		raise Exception("error finding 1 and only 1 entry in rosters for game " + \
			str(gameId) + " and player " + str(scoringPlayerId))

	scoring_player = scoring_player_query[0]

	goal_info['scoringPlayerHeadshot'] = scoring_player['headshot']
	goal_info['scoringPlayerFirstName'] = scoring_player['firstName']
	goal_info['scoringPlayerLastName'] = scoring_player['lastName']
	goal_info['scoringPlayerPositionCode'] = scoring_player['positionCode']
	goal_info['scoringPlayerSweaterNumber'] = scoring_player['sweaterNumber']

	multigoals_combed.append(goal_info)

update_collection('multigoals_combed', multigoals_combed)
