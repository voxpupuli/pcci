#!/usr/bin/env python

import datetime
import redis
import json
import yaml
import time


r = redis.StrictRedis(host='localhost', port=6379, db=0)

with open('config.yaml') as f:
    conf = yaml.load(f.read())
f.closed

retention = conf['retention']
current_time = int(time.time())
delta = 60 * 60 * 24 * retention
cutoff = current_time - delta

completed_length = r.llen('results')

# save a list of indexes to delete after we've searched
# because in palce deleting will screw up iterating
# delete things that are older than 'retention' days
indexes = []
for i in range(completed_length):
    print i
    item = json.loads(r.lindex('results', i))
    date_unix = int(item['log_path'].split('+')[3])
    print date_unix, cutoff
    if date_unix < cutoff:
        indexes.append(i)


print i
print len(indexes)
print completed_length
