import psycopg2
import time
import myutils
import requests
import json

def summary(cur) :
    total = myutils.queryValue(cur, 'SELECT COUNT(*) FROM swapi;')
    todo = myutils.queryValue(cur, 'SELECT COUNT(*) FROM swapi WHERE status IS NULL;')
    good = myutils.queryValue(cur, 'SELECT COUNT(*) FROM swapi WHERE status = 200;')
    error = myutils.queryValue(cur, 'SELECT COUNT(*) FROM swapi WHERE status != 200;')
    print(f'Total={total} todo={todo} good={good} error={error}')

conn = psycopg2.connect(host='pg.pg4e.com',
        port=5432,
        database='pg4e_d2be0b613b', 
        user='pg4e_d2be0b613b', 
        password='pg4e_p_4ea940f9b57cdb5', 
        connect_timeout=3)
cur = conn.cursor()

defaulturl = 'https://pokeapi.co/api/v2/pokemon'
print('If you want to restart the spider, run')
print('DROP TABLE IF EXISTS pokeapi CASCADE;')
print(' ')

sql = '''
CREATE TABLE IF NOT EXISTS pokeapi
(id INTERGER, body JSONB,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ);
'''

print(sql)
cur.execute(sql)

sql = 'SELECT COUNT(url) FROM pokeapi;'
count = myutils.queryValue(cur, sql)
if count < 1:
    objects = ['films', 'species', 'people']
    for obj in objects:
        sql = f"INSERT INTO pokeapi (url) VALUES ( 'https://pokeapi.co/api/v2/pokemon?limit=100&offset=0' )";
        print(sql)
        cur.execute(sql, (defaulturl))
    conn.commit()
many = 0
count = 0
chars = 0
fail = 0
summary(cur)
while True:
    if ( many < 1 ) :
        conn.commit()
        sval = input('How many records:')
        if ( len(sval) < 1 ) : break
        many = int(sval)

    sql = 'SELECT url FROM pokeapi WHERE status IS NULL LIMIT 1;'
    url = myutils.queryValue(cur, sql)
    if url is None:
        print('No more records')
        break

    text = "None"
    try:
        print('=== Url is', url)
        response = requests.get(url)
        text = response.text
        print('=== Text is', text)
        status = response.status_code
        sql = 'UPDATE pokeapi SET status=%s, body=%s, updated_at=NOW() WHERE url = %s;'
        row = cur.execute(sql, (status, text, url))
        count = count + 1
        chars = chars + len(text)
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page",url)
        print("Error",e)
        fail = fail + 1
        if fail > 5 : break
        continue

    todo = myutils.queryValue(cur, 'SELECT COUNT(*) FROM pokeapi WHERE status IS NULL;')
    print(status, len(text), url, todo)

    # TODO: Add try/except Once we figure out what goes wrong
    js = json.loads(text)

    # Look through all of the "linked data" for other urls to retrieve
    links = ['name', 'url']
    for link in links:
        stuff = js.get(link, None)
        if not isinstance(stuff, list) : continue
        for item in stuff:
            sql = 'INSERT INTO pokeapi (url) VALUES ( %s ) ON CONFLICT (url) DO NOTHING;';
            cur.execute(sql, (item, ))

    many = many - 1
    if count % 25 == 0 :
        conn.commit()
        print(count, 'loaded...')
        time.sleep(1)
        continue

print(' ')
print(f'Loaded {count} documents, {chars} characters')

summary(cur)

print('Closing database connection...')
conn.commit()
cur.close()




















