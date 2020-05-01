import configparser
from elasticsearch import Elasticsearch
import jmespath
import json
from os import listdir
from os.path import isfile, join, splitext

# get parameters from ini file
config = configparser.ConfigParser()
config.read('config.ini')
cnf = config['DEFAULT']

outfilenames = []
mappings = []
indices = set()


def dump_content(filename, str_content):

    # gets the json inside the EXTRACTPATH (most likely hits.hits[*])
    hits = jmespath.search(cnf['EXTRACTPATH'], str_content)

    # writes 2 lines, required by the BULK API
    def dumpline(h):
        indices.add(h['_index'])
        return ('{"index":{"_index":"' + h['_index'] + '","_id" :"' + h['_id'] + '"}}\n' +
                json.dumps(h['_source'], ensure_ascii=False) + '\n')

    lines = [dumpline(h) for h in hits]

    filename = 'out_' + filename + '.json'
    outfilenames.append(filename)

    with open(filename, 'w', newline='\n', encoding="utf8") as outfile:
        outfile.writelines(lines)

    print('written file ' + filename + ' (' + str(len(hits)) + ' entries)')


if cnf.getboolean('USEFILE'):
    # get the file (or list of files if using prefix)
    filenames = [f for f in listdir('.') if f.startswith(
        cnf['INPUTFILE'])] if cnf.getboolean('USEPREFIX') else [cnf['INPUTFILE']]

    # rprocess and dump the files one-by-one
    for f in filenames:
        with open(f, 'r', encoding="utf8") as content_file:
            filename, ext = splitext(f)
            dump_content(filename, json.loads(content_file.read()))
else:
    # get data from a URL

    # get the list of index patterns to search
    patterns = list(map(str.strip, cnf['INDICES'].split(',')))

    # connect to elastic ignoring ssl check. user/pass, if any, should be inculded in the url
    es = Elasticsearch([cnf['URL']], verify_certs=False)

    # search, process and dump index patterns one-by-one
    for ind in patterns:
        if cnf.getboolean('INCLUDEMAPPINGS'):
            m = es.indices.get_mapping(index=ind)
            ms = jmespath.search('*.mappings.properties', m)
            mappings.append((ind, str(ms[0]).replace("'", '"')))

        resp = es.search(index=ind, size=cnf.getint('MAXQUERY'))
        filename = ind.strip('*')
        dump_content(filename, resp)

if cnf.getboolean('GENERATEUPLOADSCRIPT'):
    lines = ['#!/bin/bash']

    if cnf.getboolean('INCLUDEINDICES'):
        lines.append('\n\necho "puting indices..."')
        s = "\ncurl -X PUT " + cnf['TARGETURL'] + "/"
        lines = lines + list([s + i for i in indices])

    if cnf.getboolean('INCLUDEMAPPINGS'):
        lines.append('\n\necho "puting mappings..."')
        s = "\ncurl -X PUT " + \
            cnf['TARGETURL'] + \
            "/{0}/_mapping -H 'Content-Type: application/json' -d'{{\"properties\":{1}}}'"
        lines = lines + list([s.format(m[0], m[1]) for m in mappings])

    lines.append('\n\necho "posting data..."')
    s = "\ncurl -o /dev/null -X POST " + \
        cnf['TARGETURL'] + "/_bulk  -H 'Content-Type: application/json' --data-binary '@"
    lines = lines + list([s + f + "'" for f in outfilenames])

    with open("setup.sh", 'w', newline='\n', encoding="utf8") as outfile:
        for line in lines:
            outfile.write(line)
