
import psycopg2

conn = psycopg2.connect(host='pg.pg4e.com',
        port=5432,
        database='pg4e_d2be0b613b', 
        user='pg4e_d2be0b613b', 
        password='pg4e_p_4ea940f9b57cdb5', 
        connect_timeout=3)

cur = conn.cursor()

sql = 'DROP TABLE IF EXISTS pythonseq CASCADE;'
print(sql)
cur.execute(sql)

sql = 'CREATE TABLE pythonseq (iter INTEGER, val INTEGER);'
print(sql)
cur.execute(sql)

number = 399492

for i in range(300) :
    print(i+1, number)   
    sql = 'INSERT INTO pythonseq (iter, val) VALUES (%s, %s);'
    conn.commit()     
    cur.execute(sql, (i, number))
    number = int((number * 22) / 7) % 1000000
conn.commit()