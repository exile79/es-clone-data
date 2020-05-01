# es-clone-data
esfetch.py uses ElasticSearch data (fetched from a url or from a file) to generate data ready to be uploaded using the [BULK API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

Configuration using the config.ini file
---
[DEFAULT]

* USEFILE: True/False, if False script will use the URL instead of loacl file
* USEPREFIX: True/False, if False, INPUTFILE is used as it is, otherwise all files that start with it will be used (ex. input_01.json, input_02.json, input_foo.json...)
* INPUTFILE: full filename if USEPREFIX=False, prefix otherwise
* EXTRACTPATH:  the json path to extract from the input files, (example hits.hits[*])
* URL: The cluser url, including port, username and password. Used if USEFILE=False. Example https//user:pass@localhost:9200
* INDICES: index patterns to fecth from Url, comma separated. Example index1*,logstash*,foo*. Script will generate one output file per index pattern.
* MAXQUERY: Size of the query results
* GENERATEUPLOADSCRIPT: True/False, to create or nor a bash script for uploading the data generated
* INCLUDEINDICES: True/False If creation of the correspondinfg indices shoud be included in the load bash script
* INCLUDEMAPPINGS: True/False if putting of mappings shoudl be included for ht ecreated inidces. Mappings are fetched from url in separate query
* TARGETURL: The url of the target cluster to use in the bash load script, Example http://localhost:9200


Query to import the resulting data
---
Example:
```
curl -X POST http://localhost:9200/_bulk  -H 'Content-Type: application/json' --data-binary "@output.json"