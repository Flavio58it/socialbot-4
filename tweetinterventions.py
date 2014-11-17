import twitter

import json
from datetime import datetime, timedelta
import sys
from time import sleep
from numpy.random import exponential

def retweet_by_id(api, twt):
		try:
			api.statuses.retweet(id=twt['id'])
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print "Unexpected error:", str(sys.exc_info())
			pass

bots = [2787456828, 2795790799, 2786086363, 1727908398, 2749655899, 2787498932, 2787463746, 2787527221, 2787481304, 1879311937, 2786427865, 2787610574, 2787474126, 2787905696, 2787485774, 2787531548, 2787514615, 2787482192, 2801335412, 2787503576, 2802511814, 2787620990, 2787486036, 2787486060, 2787499142, 197886036, 2829847496, 2786363222, 2787833887]

keys = json.loads(file('auth.json').read())
auth = twitter.OAuth(keys['OAUTH_TOKEN'], keys['OAUTH_TOKEN_SECRET'], keys['APP_KEY'], keys['APP_SECRET'])
api = twitter.Twitter(auth=auth)

format_day = '%d-%m-%Y'
format_hours = '%H:%M'
format_full = format_day + ' ' + format_hours

tweet_scheme = {'14-11-2014':{'twts':['some_tweet_goes_here'], 
								'hsh': ['#getyourflushot', '#igotminetoday'],
								'tweet_times': ['18:36', '23:54']},
				'12-11-2014':{'hsh': ['#newinsf', '#sfgiants']}
				'17-11-2014':{'hsh': ['#highfiveastranger']}				
				}


today = datetime.now().strftime(format_day)
tomorrow = (datetime.now() + timedelta(1)).strftime(format_day)
#exit if not a proper tweet day.
if today not in tweet_scheme:
	sys.exit(0)

now = datetime.now()
max_twt_id = 0
bot_rts = 0
wait_interval = 60
cycle_length = 30

# Each cycle is in 30 minutes.
while now < datetime.strptime(tomorrow + ' 08:00', format_full):
	print tomorrow + ' 08:00'
	start = datetime.now()
	twts = []
	for hsh in tweet_scheme[today]['hsh']:
		twts.extend(api.search.tweets(q=hsh, since_id = max_twt_id, count = 30)['statuses'])
	
	bot_tweets = [twt for twt in twts if twt['user']['id'] in bots]
	humantweets = [twt for twt in twts if twt['user']['id'] not in bots]
	for twt in bot_tweets:
		while bot_rts < 10:
			sleep(exponential(wait_interval))
			retweet_by_id(api,twt)
			#print 'rt: ' + str(twt['text'])
			bot_rts += 1

	count = 0
	for twt in humantweets:
		sleep(exponential(wait_interval))
		retweet_by_id(api,twt)
		#print 'rt: ' + twt['text']
		count += 1
		if count > 14:
			count = 0
			sleep(120)

	# Wait till at least 20min have passed since last fetch of tweets.
	minutes_since = (datetime.now() - start).seconds/wait_interval
	if minutes_since < cycle_length:
		print 'Waiting: ' + str(30 - minutes_since) + 's'
		if len(twts) > 0:
			max_twt_id = max([twt['id'] for twt in twts])
		sleep((cycle_length - minutes_since)*60)
	now = datetime.now()
