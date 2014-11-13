import json





f = open('/home/ubuntu/data/tried_to_follow.json','r')

lines = f.read().split('\n')[:-1]

records = []

for line in lines:
	records.append(json.loads(line))

print records


