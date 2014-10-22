import json
import twitter
import json
import time
from datetime import datetime
from numpy import random
import urllib

class Actor(object):
	def __init__(self,path='/home/ubuntu/'):
			keys = json.loads(file(path + 'auth.json').read())

			auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
                            keys['APP_KEY'], keys['APP_SECRET'])

			self.api = twitter.Twitter(auth=auth)
			self.path = path
			self.format = '%Y-%d-%m %H-%M-%S'

	def unfollow(self, count = 1):
		bad_friends = json.load(open(self.path + 'data/bad_friends.json'))
		for i in range(count):
			if len(bad_friends) > 0:
				usr_id = bad_friends.pop()
				print 'Destroying friendship: ' + str(usr_id)
				self.api.friendships.destroy(user_id = usr_id)
				fp = open(self.path + 'data/hiriactivity.log', 'a')
				fp.write(datetime.strftime(datetime.now(), self.format) + ' unfol ' + str(usr_id) + '\n')
				fp.close()
		if len(bad_friends) == 0:
			bad_friends = []
		json.dump(bad_friends, open(self.path + 'data/bad_friends.json','wb'))
		return count     # no. api calls

	def follow(self, favoritetwt = True, count = 1):
		new_friends = json.load(open(self.path + 'data/new_friends.json'))
		for i in range(count):
			if len(new_friends) > 0:
				usr_id = new_friends.pop()
				self.api.friendships.create(user_id = usr_id)
				print 'Created friendship: ' + str(usr_id)

				fp = open(self.path + 'data/hiriactivity.log', 'a')
				fp.write(datetime.strftime(datetime.now(), self.format) + ' fol ' + str(usr_id) + '\n')
				fp.close()
				
				fp = open(self.path + 'data/tried_to_follow.json', 'a')
				res = self.api.users.lookup(user_id = usr_id)
				fp.write(json.dumps(res[0]) + '\n')
				fp.close()
				if favoritetwt:
					status = self.api.statuses.user_timeline(user_id=usr_id, count = 1)[0]  # can be extended to favorite random twt
					fav_fp = open(self.path + 'data/to_favorite.json', 'a')
					json.dump({'id':status['id'], 'usr_id':usr_id},fav_fp)
					fav_fp.write('\n')
		if len(new_friends) == 0:
			new_friends = []
		json.dump(new_friends, open(self.path + 'data/new_friends.json','wb'))
		calls = count 
		if favoritetwt:
			calls += count
		return calls  # no. api calls

	def favoritePost(self, count = 1):  # Error in api ?
		#to_favorite = json.load(open(self.path + 'data/to_favorite.json'))
		to_favorite = [json.loads(line) for line in open(self.path + 'data/to_favorite.json') if line != '\n']
		for i in range(min(count, len(to_favorite))):
			fav_twt = to_favorite.pop()
			print 'Favoriting status: ' + str(fav_twt['id'])
			self.api.favorites.create(_id = fav_twt['id'])
			fp = open(self.path + 'data/hiriactivity.log', 'a')
			fp.write(datetime.strftime(datetime.now(), self.format) + ' fav ' + str(fav_twt['usr_id']) + '\n')
			fp.close()
		if len(to_favorite) == 0:
			to_favorite = []
		fp = open(self.path + 'data/to_favorite.json', 'wb')
		for fav in to_favorite:
			json.dump(fav,fp)
			fp.write('\n')
		return count # no. api calls

	def postTwt(self, lat = 37.783333, lon = -122.416667):
		twts = [json.loads(line) for line in open(self.path + 'data/to_tweet.json') if line != '\n']
		lat = lat + random.normal(0,0.02)
		lon = lon + random.normal(0,0.02)
		if len(twts) > 0:
			twt = twts.pop()
			fp = open(self.path + 'data/to_tweet.json','wb')
			for twt in twts:
				json.dump(twt,fp)
				fp.write('\n')	
			fp.close()
			#print 'Posting twt: ' + twt['text']
			if 'media_url' in twt:
				img = urllib.urlopen(twt['media_url']).read()
				params = {'status':twt['text'], 'media[]':img, 'lat':str(lat), 'long':str(lon)}
				self.api.statuses.update_with_media(**params)
			else:
				self.api.statuses.update(status = twt['text'], lat = lat, long=lon)
		return 1  # no. api calls

	def retweet(self): #test method
		retwts = json.load(open(self.path + 'data/retweets.json'))
		if len(retwts) > 0:
			twt = retwts.pop()
			print 'Retweeting: ', twt
			self.api.statuses.retweet(id=twt)
		json.dump(retwts,open(self.path + 'data/retweets.json','wb'))
		return 1

	def send_log(self, method):
		msg = "Running routine", datetime.now(), method
		self.api.direct_messages.new(screen_name="SuperRexy",text=msg)

	def write_log(self, method):
		#discontinued
		msg = "Running routine", datetime.now(), method, '\n'
		print msg
		open(self.path + 'data/hiri.log','a').write(str(msg))


if __name__ == '__main__':
	pass


