import json
import twitter
import pickle

class Actor(object):
        def __init__(self,path="../auth.json"):
                keys = json.loads(file(path).read())

                auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
                                keys['APP_KEY'], keys['APP_SECRET'])

                self.api = twitter.Twitter(auth=auth)

        def unfollow(self, count):
        	bad_friends = pickle.load(open('../bad_friends.pkl'))
        	for i in range(count):
        		usr = bad_friends.pop()
        		self.api.friendships.destroy(user_id = usr.id)




a = Sensor()