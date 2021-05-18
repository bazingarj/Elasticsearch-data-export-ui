from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'eventName': 'event_a',
    'eventValue': {"custom_key":1},
    'timestamp': datetime.now(),
}

index= 'logs'
total= 11000

for i in range(5000,total):
	res = es.index(index=index, id=i, body=doc)
	#print(res['result'])

