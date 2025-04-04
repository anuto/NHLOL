from mongo_wrapper import *

games_cursor = get_collection('games')

mistake_ids = []

for game in games_cursor:
	game_id = game['_id']
	if not isinstance(game_id, int):
		mistake_ids.append(game_id)
		print(str(game_id))
	else:
		print(".", "")

print("total: " + str(len(mistake_ids)))

db = get_db()
games = db['games']

for mistake_id in mistake_ids:
	games.delete_one({"_id": mistake_id})