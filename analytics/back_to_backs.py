from db.mongo_wrapper import *
from datetime import datetime, timedelta

ONE_DAY = timedelta(days = 1)

print("getting teams...")
teams = get_collection('teams')

print("getting games...")
games = get_raw_collection('games')

team_back_to_backs_counter = {}
team_back_to_backs = {}

for team_info in teams:

	team = team_info['_id']
	team_name = team_info['abbrev']

	print("processing team " + team_name + "...")

	team_games = games.find(
		{
			'$and': [
				{
					'$or': [
						{'homeTeamId': team},
						{'awayTeamId': team}
					]
				},
				{'gameType': 2}
			]
		}
	)

	game_dates = []

	for game in team_games:
		gameDateField = game['gameDate']
		game_date = datetime.strptime(gameDateField, "%Y-%m-%d")
		game_dates.append((game_date, game))

	if game_dates:
		game_dates_sorted = sorted([game[0] for game in game_dates])

		last_game_date = None
		back_to_backs = []

		for game_date in game_dates_sorted:
			print(game_date)
			if last_game_date:

				time_off = game_date - last_game_date

				if time_off == ONE_DAY:
					game = [game for (game_date, game) in game_dates][1]
					back_to_backs.append(game)

			last_game_date = game_date

		team_back_to_backs[team_name] = back_to_backs
		team_back_to_backs_counter[team_name] = len(back_to_backs)

print(dict(sorted(team_back_to_backs_counter.items(), key=lambda item: item[1])))

