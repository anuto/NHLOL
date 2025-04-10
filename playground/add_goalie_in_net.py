from db.mongo_wrapper import *
import requests
from db_scripts.backfill_from_play_by_plays import get_play_by_play_url

print("getting goals table...")
goals_table = get_raw_collection('goals')

print("getting all goals...")
# goals = goals_table.find({"goalieId": {"$exists": False}})
goals = goals_table.find()
print("getting all game ids....")
game_ids = goals.distinct('gameId')

for game_id in game_ids:
	print("processing game " + str(game_id))

	url = get_play_by_play_url(game_id)
	print(url)

	response = requests.get(url)
	game_info = response.json()

	if 'plays' in game_info:
		plays = game_info['plays']

		for play in plays:
			if 'typeDescKey' in play and play['typeDescKey'] == 'goal':
				goal = play

				if 'details' in goal:
					details = goal['details']

					if 'goalieInNetId' in details:
						goalie_id = details['goalieInNetId']
						event_id = play['eventId']


						print("updating " + str(event_id))
						goals_table.update_one(
							{'$and': [
								{'gameId': game_id},
								{'eventId': event_id}	
							]},
							{
								'$set': {
									'goalieId': goalie_id
								}
							}
						)