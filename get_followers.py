
import twitter
import json
from time import sleep


def get_fols():
	keys = json.loads(file('/home/ubuntu/auth.json').read())

	auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
	keys['APP_KEY'], keys['APP_SECRET'])

	api = twitter.Twitter(auth=auth)

	followers = api.followers.ids()['ids']

	return followers


