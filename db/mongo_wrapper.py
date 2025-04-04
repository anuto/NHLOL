from db.secrets.mongo import MONGO_URI, DB_NAME
import pymongo

def get_db():
	client = pymongo.MongoClient(MONGO_URI)
	try:
		client.admin.command('ping')
	except ConnectionFailure:
		print("Server not available.")

	return client[DB_NAME]


def get_collection(collection_name):
	db = get_db()
	collection = db[collection_name]

	cursor = collection.find()
	return cursor

def update_players_collection(collection_name, data):
	db = get_db()
	collection = db[collection_name]

	for row in data:
		keys = {'gameId': row['gameId'], 'playerId': row['playerId']}

		collection.replace_one(
			keys,
			row,
			upsert = True
		) 
	
	print("updated collection: " + collection_name + "!")

def update_goals_collection(collection_name, data):
	db = get_db()
	collection = db[collection_name]

	for row in data:
		keys = {'gameId': row['gameId'], 'eventId': row['eventId']}
		collection.replace_one(
			keys,
			row,
			upsert = True
		) 
	
	print("updated collection: " + collection_name + "!")



# fields_to_add: {updated_field: value}
def add_fields_to_document_in_collection(collection_name, game_id, fields_to_add):
	db = get_db()
	collection = db[collection_name]

	collection.update_one(
		{'_id': game_id},
		{'$set': fields_to_add},
		upsert = True
	)

def update_collection(collection_name, data):
	db = get_db()
	collection = db[collection_name]

	for row in data:
		collection.replace_one(
			{'_id': row['_id']},
			row,
			upsert = True
		) 
	
	print("updated collection: " + collection_name + "!")

def update_collection_with_dictionary(collection_name, data):
	db = get_db()
	collection = db[collection_name]

	for _id in data:
		row = data[_id]
		collection.replace_one(
			{'_id': row['_id']},
			row,
			upsert = True
		) 
	
	print("updated collection: " + collection_name + "!")

