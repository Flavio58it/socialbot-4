
import twitter
import json
from time import sleep



keys = json.loads(file('/home/ubuntu/auth.json').read())

auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
keys['APP_KEY'], keys['APP_SECRET'])

api = twitter.Twitter(auth=auth)

followers = api.followers.ids()['ids']

f = open('/home/ubuntu/data/followers.json','wb')
f.write(json.dumps(followers))
f.close()


