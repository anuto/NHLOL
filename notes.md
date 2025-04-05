id also like to know how often a b2b goal -> victory. need to look at gameoutcome too. yawn

hmm. need a way to check ALL back to back goals, not just only doubles. we have that data in quadras and triples, for example, which are exponentially smaller...do we just run through all of them...? 

> they shouldn't be double counted by how we've set things up. so it shouldn't be too bad. for example, a quadra can be 3 double goals as well. maybe.

good games to check correctness on:
- 2024020895
- 2024020764
- 2024020726
- 2024020011

> 1312 regulation games at this point.

> we need a backfill and daily run procedure...

> 1972 regulation time goals on in season games

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