* testing backfill

04-03 2024021205, 2024021204

{'gameDate': '2025-04-03'}

[2024021197, 2024021198, 2024021199, 2024021200, 2024021201, 2024021202, 2024021203, 2024021204, 2024021205]

good stuff. automated for processing yesterday, now.

* id also like to know how often a b2b goal -> victory. need to look at gameoutcome too. yawn

* good games to check correctness on:
- 2024020895
- 2024020764
- 2024020726
- 2024020011

* we need a backfill and daily run procedure...
=> need to add a script to run as a cron job to update specifically only today's games 

* `https://api.nhle.com/stats/rest/en/franchise?` <- active franchises