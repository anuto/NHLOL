from datetime import date, timedelta
from backfill_from_play_by_plays import update_games

yesterday = date.today() - timedelta(days = 1)
BACKFILL_DATE = yesterday.strftime("%Y-%m-%d") 

# BACKFILL_DATE = '2025-04-03'

update_games({'gameDate': BACKFILL_DATE})


