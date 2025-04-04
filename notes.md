`https://api.nhle.com/stats/rest/en/franchise?` <- active franchises

* need to add a script to run as a cron job to update specifically only today's games 

* maybe we can try one final table with something like...goals, but with an additional column for ...

-> the thing that is hard about using underlying data here is: how do we keep it loose enough that we can run under different constraints? ex.

- any unanswered goal combo
- within a time frame
	* within a time frame doesn't really apply to a break in between, since we're measuring momentum
- within the same period

hm. so. for goal in all_goals_in_game:

> only add if you scored last. 
> can't report actual combo. just time_delta since last team goal (unless it wasn't in the same period)

then this new table of "combo_goals" should have
- row for every combo goal
- time_delta for how long ago (can use to measure how long ago in this period we scored)
	- if this is empty, then we must've scored in the previous period so it doesn't count

then, on combo_goals:
	- count(where game_id = game_id) 

	should give all combo goals...although not how many are in the combo. this will need to be added up manually, given that there could be interruptions in between for an opponent combo goals

	- count(where game_id = game_id AND time_last_scored IS NOT None)

	should give all the combos in the same period

	- count(where game_id = game_id AND time_last_scored < TIME_INTERVAL)

	narrowest definition of a multigoal. but most similar to lol  :P

GAMES

game_id => games

play_id (mondo uuid) => (game_id + period + time) unique => (game_id + event_id) => plays

game_id, player_id, roster

expected number of games: 1418