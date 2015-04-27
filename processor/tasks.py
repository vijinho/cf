# -*- coding: utf8 -*-
"""
Process trades
"""
import os
import json
import time
from celery import Celery
import rethinkdb as r
#from generator import generate as g
from builtins import *

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"

root_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

r.connect('localhost', 28015).repl()

from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Europe/London',
    CELERY_ENABLE_UTC=True,
)

@app.task
def get_trade(id):
    return r.db('cf').table('trades').get(id).run()

@app.task
def process_trade(id):
    trade = get_trade(id)
    if not trade:
        return False
    return trade

if __name__ == '__main__':
    pass
#    print("Start from top-level with bin/startprocessor.sh")
