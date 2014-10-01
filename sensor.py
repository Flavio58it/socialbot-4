import praw
import json
import twitter
import nltk
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
		self.whitelist = set([16174436, 197886036, 17574034])

	def bad_friends(self):
		# remove friends who do not follow back
		friends = set(self.api.friends.ids()['ids'])
		followers = set(self.api.followers.ids()['ids'])
		followers = followers.union(self.whitelist)
		bad_friends = list(friends - (friends.intersection(followers)))
		f = open(self.path + 'data/bad_friends.json','w')
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

	def postsFromReddit(self, subreddits, limit):
		if type(subreddits) != list:
			subreddits = [subreddits]
		bad_words = ['karma', 'r/', 'reddit', 'sub', 'x-post', '[', 'nsfw']

		r = praw.Reddit(user_agent='hirihiker')
		
		content = []
		
		for sub in subreddits:
			posts = r.get_subreddit(sub).get_hot(limit = limit)
		
			for post in posts:
				content.append(post)
		
		tweetables = []
		for post in content:
			if ((post.url.find('imgur') > 0 or post.url[-4:] == '.jpg' or post.url[-4:] == '.gif' or post.url[-4:] == '.png') and (post.num_comments > 0)):
				if len(post.comments[0].body + ' ' + post.url) <= 129:
					if sum(map(lambda elm: post.title.lower().find(elm) + 1, bad_words)) == 0:
						tweet = self._get_tweet(r, post)
						tweetables.append((tweet + ' ' + post.url, post.ups - post.downs))
		if len(tweetables) > 0:
			tweetables = sorted(tweetables, key=lambda twt: twt[1])
			fp = open(self.path + 'data/to_tweet.json','a')
			json.dump({'text':tweetables[-1][0]}, fp)
			fp.write('\n')
			return True
		else:
			return False

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

if __name__ == '__main__':
	s = Sensor(path='../')
