from sensor import *
import random

s = Sensor(path='../')

#s = Sensor()
hashtags = ['minecraft', 'dota2', 'leagueoflegends', 'gaming', 'gaymer', 'gamergate', 'vagante', 'indiegames', 'cosplay']
random.shuffle(hashtags)
s.new_friends(hashtags = hashtags[:3])
s.bad_friends()
s.new_top_retweet(hashtags = hashtags, count = 3)
#'sweden', 'swarje',
subreddits = ['minecraft', 'dota2', 'leagueoflegends', 'gaming']

random.shuffle(subreddits)
subreddit = subreddits.pop()
print subreddit
while not s.postsFromReddit(subreddit, limit = 10):
	print subreddit
	try:
		subreddit = subreddits.pop()
	except IndexError:
		break
