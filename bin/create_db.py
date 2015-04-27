#!/usr/bin/env python
import rethinkdb as r

r.connect('localhost', 28015).repl()

db = 'cf'
tables = ['trades', 'processed']

print("Creating database: {}").format(db)
print(r.db_create(db).run());

for table in tables:
    print("Creating table: {}").format(table)
    print(r.db(db).table_create(table).run());
