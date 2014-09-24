


import json
import twitter


class Sensor(object):
	def __init__(self,path="../auth.json"):
		keys = json.loads(file(path).read())	
		
		auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
				keys['APP_KEY'], keys['APP_SECRET'])

		self.api = twitter.Twitter(auth=auth)

	def bad_friends(self):
		# remove friends who do not follow back
		friends = set(self.api.friends.ids()['ids'])
		followers = set(self.api.followers.ids()['ids'])
		bad_friends = list(friends - (friends.intersection(followers)))
		f = open('../data/bad_friends.json','w')
		f.write(json.dumps(bad_friends))
		f.close()

	


s = Sensor()
s.bad_friends()
