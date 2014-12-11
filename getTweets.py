import twitter
import math
import pickle
import json
import urllib
import logging
import sys
import time

class Twitterapi(object):
	"""docstring for twitterapi"""
	def __init__(self, path='/home/ubuntu/'):
			keys = json.loads(file(path + 'auth.json').read())

			auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
                            keys['APP_KEY'], keys['APP_SECRET'])

			self.twitter_api = twitter.Twitter(auth=auth)
			self.path = path

	def get_user_ids(self, filename):
		user_ids = []

		for line in open(self.path + filename, "rb"):
			user_id = int(json.loads(line)["id"])
			user_ids.append(user_id)

		return user_ids

	def get_tweets_from_id(self, _id, count):
		try:
			return self.twitter_api.statuses.user_timeline(user_id = _id, count = count)
		except: 
			print sys.exc_info()
			return []

	def add_tweets_to_file(self, _id, tweets):
		f = open(self.path + "tweets.json", "a")
		f.write(json.dumps({"id": _id, "tweets": tweets}) + "\n")
		f.close()

	def main(self):
		filename = "data/tried_to_follow.json"

		get_tweets_from_ids = list(set(twitterapi.get_user_ids(filename)))
		print "Number of ids in file: %i" % len(get_tweets_from_ids)

		already_got_from_ids = twitterapi.get_user_ids("tweets.json")
		print len(already_got_from_ids)

		missing_ids = [_id for _id in get_tweets_from_ids if _id not in already_got_from_ids]
		print "Number of ids left: %i" % len(missing_ids)

		print get_tweets_from_ids
		print missing_ids
		print already_got_from_ids

		for _id in missing_ids:
			print "Get tweets from %s" % _id
			tweets = twitterapi.get_tweets_from_id(_id, 200)
			print "Number of tweets found %i" % len(tweets)

			print "Storing tweets"
			twitterapi.add_tweets_to_file(_id, tweets)
			print "Successfully stored tweets from users: %s" % _id

			#print "Sleeps for 5 secs"
			#time.sleep(5)


if __name__ == "__main__":
	import sys
	twitterapi = Twitterapi(path = '')
	twitterapi.main()

