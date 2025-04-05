from db.mongo_wrapper import *
import pdb

print("loading raw table")
multigoals_table = get_raw_collection('multigoals_combed')

# print("loading cursor")
# multigoals = get_collection('multigoals_combed')

print("finding distinct games")

pipeline = [
	{'$group': {'_id': '$gameId', "count": {"$sum": 1}}},
]

games_cursor = multigoals_table.aggregate(pipeline)
games = games_cursor.to_list()

combos = {}
for game in games:
	combo = game['count']
	if combo not in combos:
		combos[combo] = []

	combos[combo].append(game['_id'])

print(combos)
print("done")