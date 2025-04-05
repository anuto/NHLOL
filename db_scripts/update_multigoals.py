from datetime import date, timedelta
from db.mongo_wrapper import *

from write_multigoals import process_games

yesterday = date.today() - timedelta(days = 1)
# BACKFILL_DATE = yesterday.strftime("%Y-%m-%d") 

BACKFILL_DATE = '2025-04-03'

games_cursor = get_collection(
	'games', 
	{
		'gameType': 2,
		'gameDate': BACKFILL_DATE
	}
)

multigoals = process_games(games_cursor)
insert_in_collection('multigoals', multigoals)
