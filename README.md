# es-clone-data
use an Elastic search query to get data from an index and prepare a json for bulk writing to another one


Query to import the resulting data:
curl -X POST http://localhost:9200/_bulk  -H 'Content-Type: application/json' --data-binary "@output.json"