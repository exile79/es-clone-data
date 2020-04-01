import configparser
import requests
import jmespath
import json

# get parameters from ini file
config = configparser.ConfigParser()
config.read('config.ini')
USEFILE = config['DEFAULT']['UseFile']
INPUTFILE = config['DEFAULT']['InputFile']
OUTPUTFILE = config['DEFAULT']['OutputFile']
URL = config['DEFAULT']['url']
INDEX2WRITE = config['DEFAULT']['Index2Write']
TYPE2WRITE = config['DEFAULT']['Type2Write']
EXTRACTPATH = config['DEFAULT']['ExtractPath']

rj = None

if USEFILE:
    # get data from file
    with open(INPUTFILE, 'r', encoding="utf8") as content_file:
        content = content_file.read()
        rj = json.loads(content)
else:
    # get data from a URL
    r = requests.get(url=URL)
    rj = content.json()

if not rj:
    exit

h = jmespath.search(EXTRACTPATH, rj)
bulk = '{"index":{"_index":"' + INDEX2WRITE + '","_type" :"' + TYPE2WRITE + '"}}'

with open(OUTPUTFILE, 'w', newline='\n', encoding = "utf8") as outfile:
    for s in h:
        outfile.write(bulk+'\n')
        outfile.write(json.dumps(s, ensure_ascii = False) + '\n')

print('Finished. Written ' + str(len(h)) + ' entries')
