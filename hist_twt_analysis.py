import json
import regex 

fp = open('../data/historical_timeline.json')
fp_bad = open('../data/bad_hsh.json')

bad_hshs = []
for line in fp_bad.readlines():
	bad_hshs.append(line.strip())

hist = []
for line in fp.readlines():
	hist.append(json.loads(line))

hshs = {}
hsh_filter = '#\S*'

for twt in hist:
	for hsh in regex.findall(hsh_filter, twt['text'].lower()):
		if hsh not in bad_hshs:
			if hsh not in hshs:
				hshs[hsh] = 0
			hshs[hsh] += 1

sort_hshs = sorted(hshs.items(), key=lambda elm: elm[1])

'''
We can do a split up of the different types of users we engage with
	by the hashtag that each user have used.
	This way we can see what they engage with and if they are 
	a follow train or not.
NMF ~~~ fun fun fun

'''