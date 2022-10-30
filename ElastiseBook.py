import copy
import hashlib
import json
import time
import uuid

import hidden
from elasticsearch import Elasticsearch, RequestsHttpConnection

bookfile = input("Enter book file (i.e. pg18866.txt): ")
if bookfile == '' : bookfile = 'pg18866.txt';
indexname = bookfile.split('.')[0]

res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index", indexname)
print(res)

res = es.indices.create(index=indexname)
print("Created the index...")
print(res)

para = ''
chars = 0
count = 0
pcount = 0
for line in fhand:
    count = count + 1
    line = line.strip()
    chars = chars + len(line)
    if line == '' and para == '' : continue
    if line == '' :
        pcount = pcount + 1
        doc = {
            'offset' : pcount,
            'content': para
        }

m = hashlib.sha256()
m.update(json.dumps(doc).encode())
pkey = m.hexdigest()

res = es.index(index=indexname, id=pkey, body=doc)

print('Added document', pkey)
        # print(res['result'])

if pcount % 100 == 0 :
    print(pcount, 'loaded...')
    time.sleep(1)
    para = ''
    continue

    para = para + ' ' + line

# Tell it to recompute the index
res = es.indices.refresh(index=indexname)
print("Index refreshed", indexname)
print(res)

print(' ')
print('Loaded',pcount,'paragraphs',count,'lines',chars,'characters')


