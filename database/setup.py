import sqlite3 as s

db = s.connect('./test.sql')
c = db.cursor()

with open('./create_schema.sql') as f:
    c.executescript(f.read())

with open('./seed.sql') as f:
    c.executescript(f.read())

db.commit()

exit(0)
