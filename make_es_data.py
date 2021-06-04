from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'name': 'event_a',
    'value': {"custom_key":1},
    'j':'k',
    'timestamp': datetime.now()
}

index= 'logs'
startAt=0
total= 200

for i in range(startAt,total):
	res = es.index(index=index, id=i, body=doc)
	#print(res['result'])

