from db_scripts.backfill_from_play_by_plays import update_games
from db.mongo_wrapper import *
from db_scripts.write_multigoals import process_games

def update_date(date):

	games_cursor = get_collection(
		'games', 
		{
			'gameType': 2,
			'gameDate': date
		}
	)

	multigoals = process_games(games_cursor)

	games = get_collection('games', {'gameDate': date})
	game_ids = games.distinct('_id')

	rewrite_collection_for_game_ids('multigoals', multigoals, game_ids)

