#!/usr/bin/env python

import rethinkdb as r

r.connect('localhost', 28015).repl()

print(r.db('cf').table('trades').count().run())
