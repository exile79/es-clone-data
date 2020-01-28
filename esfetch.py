import requests
import jmespath
import json

# TODO get query from configuration file
URL = "http://localhost:9200/test1/_search"
INDEX2WRITE = 'test3'
TYPE2WRITE = '_doc'

# TODO try-catch exceptions
r = requests.get(url=URL)

rj = r.json()

# TODO parameterize the path we want to extract
h = jmespath.search('hits.hits[*]._source', rj)

file = open('myfile.json', 'w', newline='\n')

bulk = '{"index":{"_index":"' + INDEX2WRITE + '","_type" :"' + TYPE2WRITE + '"}}'

for s in h:
    file.write(bulk+'\n')
    file.write(json.dumps(s)+'\n')

file.close()

print('Finished. Written ' + str(len(h)) + ' entries')
