import praw
import json
import twitter
from datetime import datetime
from random import sample
from time import sleep

class Sensor(object):
	def __init__(self,path="/home/ubuntu/"):
		keys = json.loads(file(path + 'auth.json').read())	
		
		auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
				keys['APP_KEY'], keys['APP_SECRET'])

		self.api = twitter.Twitter(auth=auth)
		self.path = path

	def bad_friends(self):
		# remove friends who do not follow back
		friends = set(self.api.friends.ids()['ids'])
		followers = set(self.api.followers.ids()['ids'])
		bad_friends = list(friends - (friends.intersection(followers)))
		f = open(self.path + 'data/bad_friends.json','w')
		f.write(json.dumps(bad_friends))
		f.close()

	def postsFromReddit(self, subreddits, limit):
		if type(subreddits) != list:
			subreddits = [subreddits]
	
		r = praw.Reddit(user_agent='hirihiker')
		
		content = []
		
		for sub in subreddits:
			posts = r.get_subreddit(sub).get_hot(limit = limit)
		
			for post in posts:
				content.append(post)
		
		tweetables = []
		for post in content:
			if ((post.url.find('imgur') > 0 or post.url[-4:] == '.jpg' or post.url[-4:] == '.gif' or post.url[-4:] == '.png') and (post.num_comments > 0)):
				if len(post.comments[0].body + ' ' + post.url) <= 140:
					tweetables.append(post.comments[0].body + ' ' + post.url)
		
		idx = 0
		for twt in tweetables:
			print str(idx) +': ' + twt
			idx += 1
		print 'Please select post to tweet:'	
		idx = input()
		if type(idx) == int and idx>=0:
			pass

	def new_friends(self):
		new_friends = []
		fol_ids = self.api.followers.ids()['ids']
		selected_followers = sample(fol_ids,1)
		for fol_id in selected_followers:
			new_friends += self.api.followers.ids(user_id=fol_id)['ids']
		
		new_friends = list(set(new_friends))
		
		with open(self.path + 'data/new_friends.json','wb') as out:
			json.dump(new_friends,out)

	def new_top_retweet(self):
		twts_in_TL = self.api.statuses.home_timeline()
		twt_dic = {}
		for twt in twts_in_TL:
			twt_dic[twt['id']] = twt['retweet_count']
		sort_dic = sorted(twt_dic.items(), key = lambda elm: elm[1])
		new_retweet = [sort_dic[-1][0]]

		with open(self.path + 'data/retweets.json','wb') as out:
			json.dump(new_retweet,out)

	def test(self):
		msg = "cron job test sent at", datetime.now()
		self.api.direct_messages.new(screen_name="hirihiker",text=msg)

	def store_timeline_tweets(self, since_id = None):
		if since_id is None:
			timeline = self.api.statuses.home_timeline()
		else: 
			timeline = self.api.statuses.home_timeline(since_id=since_id)

		jsondics = []
		for twt in timeline:
			hshlist = []
			for hsh in twt['entities']['hashtags']:
				hshlist.append(hsh['text'])
			jsondics.append({"text":twt["text"], "coordinates":twt["coordinates"], "retweet_count":twt["retweet_count"], "id":twt["id"], "created_at":twt["created_at"], 'user_id':twt["user"]["id"], 'hashtags':hshlist})
		fp = open(self.path + 'data/historical_timeline.json','a')
		for twt in jsondics:
			json.dump(twt, fp)
			fp.write('\n')

if __name__ == '__main__':
	s = Sensor(path='../')
