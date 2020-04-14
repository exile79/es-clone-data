import configparser
import requests
import jmespath
import json
from os import listdir
from os.path import isfile, join,splitext

# get parameters from ini file
config = configparser.ConfigParser()
config.read('config.ini')
USEFILE = config['DEFAULT']['UseFile']
USEPREFIX = config['DEFAULT']['UsePrefix']
INPUTFILE = config['DEFAULT']['InputFile']
OUTPUTFILE = config['DEFAULT']['OutputFile']
URL = config['DEFAULT']['url']
INDEX2WRITE = config['DEFAULT']['Index2Write']
TYPE2WRITE = config['DEFAULT']['Type2Write']
EXTRACTPATH = config['DEFAULT']['ExtractPath']

rj = []

if USEFILE:
    fnames = []
    if USEPREFIX:
        fnames = [f for f in listdir('.') if f.startswith(INPUTFILE)]
    else:
        fnames = [INPUTFILE]

    for f in fnames:
        with open(f, 'r', encoding="utf8") as content_file:
            content = content_file.read()
            rj.append(json.loads(content))
else:
    # get data from a URL
    r = requests.get(url=URL)
    rj = [content.json()]

if len(rj) < 1:
    exit

hh = []
for rr in rj:
    hh.append(jmespath.search(EXTRACTPATH, rr))

bulk = '{"index":{"_index":"' + INDEX2WRITE + '","_type" :"' + TYPE2WRITE + '"}}'

cnt = 1
for h in hh:
    filename, file_extension = splitext(OUTPUTFILE)
    of = filename + str(cnt) + file_extension
    cnt = cnt + 1
    with open(of, 'w', newline='\n', encoding = "utf8") as outfile:
        for s in h:
            outfile.write(bulk+'\n')
            outfile.write(json.dumps(s, ensure_ascii = False) + '\n')
    print('Finished. Written ' + str(len(h)) + ' entries')
