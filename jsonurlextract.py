from itertools import count
import json
import urllib.request, urllib.parse, urllib.error
url = input("Enter url: ")
print("Retrieving ", url)
data = urllib.request.urlopen(url).read().decode('utf-8')
print('Retrieved', len(data), 'characters')
info = json.loads(data)

sum = 0
total = 0

for comment in info["comments"]:
    sum = sum + int(comment["count"])
    total = total + 1

print('Count:', total)
print('Sum:', sum)