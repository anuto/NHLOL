from db.mongo_wrapper import *
import requests
from db_scripts.backfill_from_play_by_plays import get_play_by_play_url

print("retrieving games...")
games_table = get_raw_collection('games')
games = games_table.find({})

video_urls = {}

for game in games:
	game_id = game['_id']
	url = get_play_by_play_url(game_id)
	print(url)

	response = requests.get(url)
	game_info = response.json()

	homeTeamScore = None
	awayTeamScore = None

	if 'awayTeam' in game_info:
		awayTeam = game_info['awayTeam']
		homeTeam = game_info['homeTeam']

		if 'score' in awayTeam:
			awayTeamScore = awayTeam['score']
			homeTeamScore = homeTeam['score']

			if homeTeamScore > awayTeamScore:
				winningTeam = game['homeTeamId']
			else:
				winningTeam = game['awayTeamId']

			games_table.update_one(
				{'_id': game['_id']},
				{'$set': {
					'homeTeamScore': homeTeamScore,
					'awayTeamScore': awayTeamScore,
					'winningTeam': winningTeam
				}}
			)

			print("updated.")

