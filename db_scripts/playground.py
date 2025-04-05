from db.mongo_wrapper import *

# checky checky
games = get_collection('games', {'gameDate': '2025-04-03'})

# all for that day
game_ids = games.distinct('_id')

# no goals yet. good. backfill time.
# game_ids = [2024021205, 2024021204]

# goals = get_collection(
# 	'goals',
# 	{
# 		'gameId': {
# 			'$in': game_ids
# 		}
# 	}
# )

# print(goals.to_list())

# rosters need backfill in case of injury / trade. 
# no idea why they're already populated.
# rosters = get_collection(
# 	'rosters',
# 	{
# 		'gameId': {
# 			'$in': game_ids
# 		}
# 	}
# )

# print(rosters.to_list())

multigoals = get_collection(
	'multigoals',
	{
		'gameId': {
			'$in': game_ids
		}
	}
)

from pprint import pprint
x = multigoals.to_list()
pprint(x)
print(len(x))
