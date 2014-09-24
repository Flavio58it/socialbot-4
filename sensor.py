


import json
import twitter


class Sensor(object):
	def __init__(self,path="../auth.json"):
		auth = json.loads(file(path).read())	
		print auth


s = Sensor()
