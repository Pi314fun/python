from cgitb import text
from email.quoprimime import body_check
import psycopg2, json, requests, myutils 
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

defaulturl = 'https://pokeapi.co/api/v2/pokemon?limit=100&offset=0'


sql = '''
CREATE TABLE IF NOT EXISTS pokeapi
(id INTEGER, url VARCHAR(2048), body JSONB); 
'''
print(sql)
cur.execute(sql)

for u in range(100):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+ str(u))
    result = response.json()
    sql = f'INSERT INTO pokeapi(id,body) VALUES({u}, {result} );'
    js_body = json.dumps()
    print(sql)
    cur.execute(sql, (defaulturl))

print('Closing database connection...')
conn.commit()
cur.close