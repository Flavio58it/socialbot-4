from sensor import *
import random

#s = Sensor(path='../')

s = Sensor()

s.new_friends()
s.bad_friends()
s.new_top_retweet()

subreddits = ['sweden', 'swarje', 'minecraft', 'dota2', 'leagueoflegends', 'gaming']
random.shuffle(subreddits)
subreddit = subreddits.pop()
print subreddit
while not s.postsFromReddit(subreddit, limit = 10):
	print subreddit
	try:
		subreddit = subreddits.pop()
	except IndexError:
		break
