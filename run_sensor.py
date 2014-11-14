from sensor import *
import random
import sys

if len(sys.argv) > 1 and sys.argv[1] == '-p':
	s = Sensor(path='../')
elif len(sys.argv) > 1 and sys.argv[1] == '-fols':
	s = Sensor()
	s.storeAllFriends()
	sys.exit(0)
else:
	s = Sensor()

hashtags = ['minecraft', 'dota2', 'leagueoflegends', 'gaming', 'gaymer', 'gamergate', 'vagante', 'indiegames', 'cosplay']

sf_hashtags = ['sfnative', 'sanfrancisco', 'sfcity', 'sf', 'sfgiants', 'onlyinsf', 'sflocal','cosplay']

random.shuffle(sf_hashtags)
# Deactivate friend collection
#s.new_friends(hashtags = sf_hashtags[:4], fol_count = 1)
s.bad_friends()
s.new_top_retweet(hashtags = sf_hashtags, count = 1)

subreddits = ['minecraft', 'dota2', 'leagueoflegends', 'gaming']
sf_subs = ['sanfrancisco', 'food', 'sfgiants']

random.shuffle(sf_subs)
subreddit = sf_subs.pop()
print subreddit
while not s.postsFromReddit(subreddit, limit = 10, force_hsh = subreddit) or not s.postsFromReddit(subreddit, limit = 10, get_hot = True, force_hsh=subreddit):
	print subreddit
	try:
		subreddit = sf_subs.pop()
	except IndexError:
		break
