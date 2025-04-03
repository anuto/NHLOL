import json

with open("kraken_games.json") as file:
	games_response = json.load(file)
	games = games_response['games']

	games = [game for game in games if game['gameType'] == 2]

	with open("kraken_in_season_games.json", "w") as write_file:
		json.dump(games, write_file)