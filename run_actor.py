import time
import twitter
import random
from actor import *
import numpy as np
import sys

initial_wait = True
if len(sys.argv) > 0 and sys.argv[1] == '-v':
	initial_wait = False
	actor = Actor(path = '../')
else:
	actor = Actor()

#initial wait:
if initial_wait:
	time.sleep(random.uniform(1,30*60))



counts = {'post':0, 'retwt':0, 'fol':0, 'unfol':0, 'fav':0}
maxes = {'post':1, 'retwt':1 , 'fol':1, 'unfol':1, 'fav':1}
methods = ['post', 'retwt', 'fol', 'unfol']
start = time.time()

while time.time() - start < 2*3600 and sum(maxes.values())-sum(counts.values()) > 0:
	probs = [maxes[key] - counts[key] for key in methods]
	probs = [1.0*elm/sum(probs) for elm in probs]
	
	method = random.choice(methods, size = 1, replace = False, p = probs)[0]
	if method == 'post':
		try:
			actor.postTwt()
		except twitter.TwitterHTTPError, e: 
			print 'Could not post tweet.'
	elif method == 'retwt':
		try:
			actor.retweet()
		except twitter.TwitterHTTPError, e: 
			print 'Could not retweet'
		#actor.favoritePost()
		#counts['fav'] += 1
		#if counts['fav'] > maxes['fav']:
		#	counts['fav'] = maxes['fav']
	elif method == 'fol':
		try:
			actor.follow(favoritetwt=False)
		except twitter.TwitterHTTPError, e: 
			print 'TwitterHTTPError: Following failed!'
	elif method == 'unfol':
		try:
			actor.unfollow()
		except twitter.TwitterHTTPError, e: 
			print 'TwitterHTTPError: Following failed!'
	elif method == 'fav':
		try:
			actor.favoritePost()
		except twitter.TwitterHTTPError, e: 
			print 'TwitterHTTPError: Favoriting failed!'
	counts[method] += 1
	if counts[method] > maxes[method]:
		counts[method] = maxes[method]
	
	wait_time = np.random.exponential(1*60)
	print method
	time.sleep(wait_time)
if counts['retwt'] == 0:
	actor.retweet()
	time.sleep(1)
if counts['post'] == 0:
	actor.postTwt()
