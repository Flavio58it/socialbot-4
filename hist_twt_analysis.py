import json
import regex 

fp = open('data/historical_timeline.json')

hist = []
for line in fp.readlines():
	hist.append(json.loads(line))

hshs = {}
hsh_filter = '#\S*'

for twt in hist:
	for hsh in regex.findall(hsh_filter, twt):
		if hsh not in hshs:
			hshs[hsh] = 0
		hshs[hsh] += 1

