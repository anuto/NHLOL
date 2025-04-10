from datetime import datetime
from db.mongo_wrapper import *

today = datetime.strptime('2025-04-10', "%Y-%m-%d")

games = get_collection('games')
games_table = get_raw_collection('games')

for game in games:
	print(game)
	game_date = datetime.strptime(game['gameDate'], '%Y-%m-%d')

	if game_date >= today:
		games_table.update_one(
			{'_id': game['_id']},
			{
				'$unset': {
					'awayTeamScore': '',
					'homeTeamScore': '',
					'winningTeam': ''
				}
			}
		)
		print("updated.")