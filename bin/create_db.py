#!/usr/bin/env python
import rethinkdb as r

r.connect('localhost', 28015).repl()

db = 'cf'
table = 'trades'

print("Creating database: {}").format(db)
print(r.db_create(db).run());

print("Creating table: {}").format(table)
print( r.db(db).table_create(table).run());
