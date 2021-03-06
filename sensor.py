import praw
import json
import twitter
import nltk
from datetime import datetime
from random import sample
from time import sleep
import random

class Sensor(object):
	def __init__(self,path="/home/ubuntu/"):
		keys = json.loads(file(path + 'auth.json').read())	
		
		auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'],
				keys['APP_KEY'], keys['APP_SECRET'])

		self.api = twitter.Twitter(auth=auth)
		self.path = path
		self.whitelist = set([16174436, 197886036, 17574034])

	def bad_friends(self):
		# remove friends who do not follow back
		friends = set(self.api.friends.ids()['ids'])
		followers = set(self.api.followers.ids()['ids'])
		followers = followers.union(self.whitelist)
		bad_friends = list(friends - (friends.intersection(followers)))
		f = open(self.path + 'data/bad_friends.json','wb')
		f.write(json.dumps(bad_friends))
		f.close()
	
	def _get_tweet(self, r, post):
		stopwords = nltk.corpus.stopwords.words('swedish') + nltk.corpus.stopwords.words('english')
		comments = praw.helpers.flatten_tree(post.comments)
		try:
			comments = [c.body for c in comments]
		except AttributeError:
			return post.title
		post_tokens = set(map(lambda elm: elm.lower(), nltk.word_tokenize(post.title))).difference(set(stopwords))
		d = {}
		for c in comments:
			tmp_tokens = map(lambda elm: elm.lower(), nltk.word_tokenize(c))
			for word in tmp_tokens:
				if word not in d:
					d[word] = 0
				d[word] += 1
		post_dic = {}
		for word in post_tokens:
			word = word.lower()
			if word not in post_dic:
				if word in d:
					post_dic[word] = d[word]
		if len(post_dic) > 0:
			hsh = sorted(post_dic.items(), key=lambda elm: elm[0])[-1][0]
			idx = post.title.lower().find(hsh)
			twt = post.title[:idx] + '#' + post.title[idx:]
			return twt
		return post.title

	def postsFromReddit(self, subreddits, limit, get_hot = False, force_hsh = None):
		if type(subreddits) != list:
			subreddits = [subreddits]
		bad_words = ['karma', 'r/', 'reddit', 'sub', 'x-post', '[', 'nsfw']
		bad_subs = ['sweden', 'swarje']
		good_hsh = ['sfnative', 'sfcity', 'sf', 'sfgiants', 'onlyinsf', 'sflocal']
		random.shuffle(good_hsh)
		hsh = good_hsh[0]
		if force_hsh is not None:
			hsh = hsh + ' #' + force_hsh

		r = praw.Reddit(user_agent='hirihiker')
		
		content = []
		
		for sub in subreddits:
			if get_hot:
				posts = r.get_subreddit(sub).get_hot(limit = limit)
			else:
				posts = r.get_subreddit(sub).get_new(limit = limit)	
			
			for post in posts:
				content.append(post)
		
		tweetables = []
		for post in content:
			if ((post.url[-4:] == '.jpg' or post.url[-4:] == '.gif' or post.url[-4:] == '.png') and (post.num_comments > 0)): #post.url.find('imgur') > 0 or
				if len(post.title + ' ' + post.url) <= 139:
					if sum(map(lambda elm: post.title.lower().find(elm) + 1, bad_words)) == 0:
						tweet = post.title + ' #' + hsh
						tweetables.append([tweet, post.url, post.ups - post.downs])
		if len(tweetables) > 0:
			tweetables = sorted(tweetables, key=lambda twt: twt[2])
			twt = tweetables[-1]
			fp = open(self.path + 'data/to_tweet.json','a')
			if twt[1].find('imgur') > 0 and twt[1].find('.jpg') < 0:
				twt[1] = twt[1] + '.jpg' 
			json.dump({'text':twt[0], 'media_url': twt[1]}, fp)
			fp.write('\n')
			return True
		else:
			return False

	def new_friends(self, hashtags=None, lat = 37.783333, lon = -122.416667, fol_count = 1):
		if hashtags is None:
			hashtags = []
		new_friends = []
		fol_ids = self.api.followers.ids()['ids']
		selected_followers = sample(fol_ids, fol_count)
		for fol_id in selected_followers:
			new_friends += self.api.followers.ids(user_id=fol_id)['ids'][:10]
		
		new_friends = list(set(new_friends))

		if len(hashtags) > 0:
			for hsh in hashtags:
				res = self.api.search.tweets(q=hsh)
				new_friends.extend([twt['user']['id'] for twt in res['statuses'] if twt['user']['friends_count'] > twt['user']['followers_count'] and twt['user']['followers_count'] < 500])
		random.shuffle(new_friends)
		
		with open(self.path + 'data/new_friends.json','wb') as out:
			json.dump(new_friends,out)

	def new_friend_by_users(self, u_name_1, u_name_2):
		'''Find union of followers of two DTU bots and add them to follow list.'''
		pass

	def new_top_retweet(self, hashtags = None, ub_criteria = 100, lat = 37.783333, lon = -122.416667, count = 1):
		if hashtags is None:
			hashtags = []

		#twts_in_TL = self.api.statuses.home_timeline()
		twts_in_TL = []
		for hsh in hashtags:
			res = self.api.search.tweets(q=hsh, lat = lat, long=lon)
			twts_in_TL.extend(res['statuses'])

		twt_dic = {}
		for twt in twts_in_TL:
			if twt['retweet_count'] < ub_criteria:
				twt_dic[twt['id']] = twt['retweet_count']
		sort_dic = sorted(twt_dic.items(), key = lambda elm: elm[1])
		new_retweets = [elm[0] for elm in sort_dic[-count:]]

		with open(self.path + 'data/retweets.json','wb') as out:
			json.dump(new_retweets, out)

	def test(self):
		msg = "cron job test sent at", datetime.now()
		self.api.direct_messages.new(screen_name="hirihiker",text=msg)

	def store_timeline_tweets(self, since_id = None):
		if since_id is None:
			timeline = self.api.statuses.home_timeline()
		else: 
			timeline = self.api.statuses.home_timeline(since_id=since_id, count=200)

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

	def storeAllFriends(self):
		friend_ids = self.api.friends.ids()
		fp = open('data/friends' + datetime.now().strftime('%Y-%d-%m') + '.json')
		json.dump(friend_ids, fp)


if __name__ == '__main__':
	s = Sensor(path='../')
	s.new_top_retweet(hashtags = 'sfnative')
