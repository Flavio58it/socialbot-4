import json
import twitter
import json
import random

class Actor(object):
        def __init__(self,path="../auth.json"):
				keys = json.loads(file(path).read())

				auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
                                keys['APP_KEY'], keys['APP_SECRET'])

				self.api = twitter.Twitter(auth=auth)

        def unfollow(self, count = 1):
        	bad_friends = json.load(open('../bad_friends.json'))
        	for i in range(count):
        		usr_id = bad_friends.pop()
        		self.api.friendships.destroy(user_id = usr_id)
        	json.dump(bad_friends, open('../bad_friends.json','wb'))

		def follow(self, favoritetwt = True, count = 1):
        	bad_friends = json.load(open('../new_friends.json'))
        	for i in range(count):
        		usr_id = bad_friends.pop()
        		self.api.friendships.destroy(user_id = usr_id)
        		if favoritetwt:
        			status = self.api.statuses.user_timeline(user_id=usr_id, count = 1)[0]  # can be extended to favorite random twt
        			to_favorite = json.load(open('../to_favorite.json'))
        			json.dump(to_favorite.append(status['id']), open('../to_favorite.json', 'wb'))
        	json.dump(bad_friends, open('../new_friends.json','wb'))

        def favoritePost(self, count = 1):
        	to_favorite = json.load(open('../to_favorite.json'))
        	for i in range(count):
        		status_id = to_favorite.pop()
        		self.api.favorites.create(id = status_id)
        	json.dump(to_favorite, open('../to_favorite.json', 'wb'))
        





a = Sensor()