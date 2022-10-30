
import psycopg2
import hidden
def secrets():
    return {"host": "pg.pg4e.com",
            "port": 5432,
            "database": "pg4e_d2be0b613b",
            "user": "pg4e_d2be0b613b",
            "pass": "pg4e_p_4ea940f9b57cdb5"}
# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(host=secrets['host'],
        port=secrets['port'],
        database=secrets['database'],
        user=secrets['user'],
        password=secrets['pass'],
        connect_timeout=3)

cur = conn.cursor()
sql = 'DROP TABLE IF EXISTS pythonseq CASCADE;'
print(sql)
cur.execute(sql)

sql = 'CREATE TABLE pythonseq (iter INTEGER, val INTEGER);'
print(sql)
cur.execute(sql)

conn.commit()    # Flush it all to the DB server

'number = 399492
for i in range(300) :
    print(i+1, number)
    sql = 'INSERT INTO pythonseq (iter) VALUES (%);'
    value = int((value * 22) / 7) % 1000000
    print(value)
    sql = 'INSERT INTO pythonseq (val) VALUES (value);'
    cur.execute(sql, (iter, val))
conn.commit()
