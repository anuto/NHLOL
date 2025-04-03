from secrets.mongo import MONGO_URI, DB_NAME
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

