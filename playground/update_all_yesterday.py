from datetime import date, timedelta
from db_scripts.backfill_from_play_by_plays import update_games

from db_scripts.update_yesterday import update_date

yesterday = date.today() - timedelta(days = 1)
YESTERDAY = yesterday.strftime("%Y-%m-%d") 

date = YESTERDAY

update_games({'gameDate': date})

update_date(date)

