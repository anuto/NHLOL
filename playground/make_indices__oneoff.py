from db.mongo_wrapper import *

# rosters = get_raw_collection('rosters')
# rosters.create_index([('gameId', pymongo.ASCENDING), ('playerId', pymongo.ASCENDING)])

# goals = get_raw_collection('goals')
# goals.create_index([('gameId', pymongo.ASCENDING)])

games = get_raw_collection('games')
games.create_index([('gameType', pymongo.ASCENDING)])