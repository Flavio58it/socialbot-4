


import json
import twitter


class Sensor(object):
	def __init__(self,path="../auth.json"):
		keys = json.loads(file(path).read())	
		
		auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
				keys['APP_KEY'], keys['APP_SECRET'])

		self.api = twitter.Twitter(auth=auth)


	


s = Sensor()
