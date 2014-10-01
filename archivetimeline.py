import sensor
import json

path = '../'
path = '/home/ubuntu/'

twts = [json.loads(line) for line in open(path + 'data/historical_timeline.json')]
if len(twts)>0:
	max_id = max([twt['id'] for twt in twts])
else:
	max_id = 0

s = sensor.Sensor(path = path)
s.store_timeline_tweets(since_id = max_id)