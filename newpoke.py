import psycopg2
import json
import requests

conn = psycopg2.connect(host='pg.pg4e.com',
        port=5432,
        database='pg4e_d2be0b613b',
        user='pg4e_d2be0b613b',
        password='pg4e_p_4ea940f9b57cdb5',
        connect_timeout=3)


#assign cursor
cur = conn.cursor()

#target url with limit assigned
defaulturl = 'https://pokeapi.co/api/v2/pokemon?limit=100&offset=0'

#changed id to serial
sql = '''CREATE TABLE IF NOT EXISTS pokeapi(id SERIAL, body JSONB);'''

#print everything to the postgresql database
print(sql)
cur.execute(sql)

#using json to serialize requests
response = requests.get(defaulturl)
js = response.json()

#utilizing js 'results'
results = js['results']


#loop to get value of url and insert into body
for x in range(len(results)):
    body = requests.get(results[x]['url'])
    js_body = json.dumps(body)
    sql = f"INSERT INTO pokeapi (body) VALUES ('{js_body}'::JSONB)";
    cur.execute(sql, (defaulturl))

print('Closing database connection...')
conn.commit()
cur.close()