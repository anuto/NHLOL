from db.mongo_wrapper import *
from db_scripts.get_video_url import get_video_url

print("retrieving goals...")
goals_table = get_raw_collection('goals')
# goals = goals_table.find()
goals = goals_table.find({
	'$and':[
		{"videoUrl": None},
		{'highlightClipSharingUrl': {'$ne': None}},
		{'periodNumber': {'$lte': 3}}
	]
})

# for goal in goals:
# 	if not goal['videoUrl'] and goal['periodNumber'] <= 3:
# 		url = goal['highlightClipSharingUrl']
# 		if url:
# 			print(url)
# 			video_url = get_video_url(url)

# 			print("updating " + str(goal))
# 			goals_table.update_one(
# 				{'_id': goal['_id']},
# 				{'$set': {'videoUrl': video_url}}
# 			)
# 		else:
# 			print("no url")

urls = set([])

for goal in goals:
	print(goal['gameId'])
	url = goal['highlightClipSharingUrl']
	print(url)
	urls.add(url)
	print()

print(str(len(urls)))

for url in urls:
	print(get_video_url(url))