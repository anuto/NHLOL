from datetime import date, timedelta
from backfill_from_play_by_plays import update_games
from db.mongo_wrapper import *
from write_multigoals import process_games

yesterday = date.today() - timedelta(days = 1)
YESTERDAY = yesterday.strftime("%Y-%m-%d") 
YESTERDAY = '2025-04-03'
update_games({'gameDate': YESTERDAY})

games_cursor = get_collection(
	'games', 
	{
		'gameType': 2,
		'gameDate': YESTERDAY
	}
)

multigoals = process_games(games_cursor)

games = get_collection('games', {'gameDate': YESTERDAY})
game_ids = games.distinct('_id')

rewrite_collection_for_game_ids('multigoals', multigoals, game_ids)

