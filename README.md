
# Pipeline Design

- `teams`: team_id => team_abbrev and such from schedule data
> maybe can flesh this out more later.

-  `games`: game_id => game info from schedule data, populated for each team, then expanded through play by play data. Idealist design for clarity would have games / games_expanded to have a 1:1 parity between gen_ scripts and tables, but we have a 500 MB constraint so updating the table it is 

- `goals`: all the plays in a game that are of `type_desc` = `goal`. Plays are pretty widely defined, from period markers to hits to shot attempts/blocked, etc, with vastly different metadata depending. For every game there are usually 3-12 goals with maybe an avg of 6 (complete guesstimate). There are also usually 200-300 plays. Filtering down to just goals lets us process smoothly, and cut down output by a magnitude of like...50

not to mention, no current use for the other plays

not to mention, it's already pretty slow. Took some number of hours to pull this. luckily, it is a one and done type thing, outside of the daily updates.

- `rosters`: this is horribly inefficient but I'm not sure what else to do. Maybe we can just pulls this data when needed?? Maybe?? But it's tough because there's no quick lookup as far as others have found in the API so far.

currently we store 38 rows for every `game_id` with each listed player + their team affiliation

we can't just use current roster data because people switch teams and stuff.

we also don't compute this on the fly, like, ever. but i do have concerns about slowing down the runtime by bloating the # of columns in the db, not to mention, it's super dumb to store all the data associated with each player - headshot, sweater number, etc etc, for each play as well. 

this is for the best for now. in the grand scheme of things it doesn't take up much data, just a relatively decent amount for the free tier. i could see this being a bottleneck in the future if we decide to capture other seasons.

- `multigoals`: the most application specific table. It:

- only looks at `in-season` games, currently. This is to avoid pre-season games tainting ma statz

- for every `game_id`, scores some basic info about each `combo` of goals. 

-- a `combo`: unanswered goals. Goals scored back to back by the same team. 

-- for each game in a `combo`, we store 
 * `scoringTeamId`
 * `scoringPlayerId`
 * `periodNumber`
 *  `timeInPeriod`

This gives us the ability to quickly see who's scoring (player / team). We're also able to get more info quickly about the team / game through joining to other tables.

- ex. pulling headshots for ui or team logos

By storing the combo and the period / time information, we're also able to filter on the fly, either further splitting combos by period or by time elapsed between goals.


# UUIDS

GAMES

game_id => games

play_id (mondo uuid) => (game_id + period + time) unique => (game_id + event_id) => plays

game_id, player_id, roster

# Table Cardinality:

- expected number of `games`: 1418
- expected number of in-season `games`: 1312
- expected number of `goals` in `games`: ~8k
- expected number of `multigoals`: ~1800