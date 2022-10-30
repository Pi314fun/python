import json
import psycopg2
import requests
import myutils


conn = psycopg2.connect(host='pg.pg4e.com',
        port=5432,
        database='pg4e_d2be0b613b', 
        user='pg4e_d2be0b613b', 
        password='pg4e_p_4ea940f9b57cdb5', 
        connect_timeout=3)

cur = conn.cursor()

defaulturl = 'https://pokeapi.co/api/v2/pokemon/1/'
sql = 'DROP TABLE pokeapi CASCADE;'
print(sql)
cur.execute(sql)
sql = 'CREATE TABLE IF NOT EXISTS pokeapi (id SERIAL, url VARCHAR(2056) body JSONB);'
print(sql)

sql = 'SELECT COUNT(body) FROM pokeapi;'
count = myutils.queryValue(cur, sql)
if count < 1:
    objects = ['films', 'species', 'people']
    for obj in objects:
        sql = f"INSERT INTO pokeapi (url, body) VALUES ( 'https://pokeapi.co/api/v2/{obj}/1/' )";
        print(sql)
        cur.execute(sql, (defaulturl))
    conn.commit()

    print('Closing database connection...')
conn.commit()
cur.close() 

