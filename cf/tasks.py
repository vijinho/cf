# -*- coding: utf8 -*-
"""
Process trades
"""
import os
import json
import time
from celery import Celery
import rethinkdb as r
#from cf import generate as g
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

from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Europe/London',
    CELERY_ENABLE_UTC=True,
)

def database(func):
    def connect(*args, **kwargs):
        r.connect('localhost', 28015).repl()
        return func(*args, **kwargs)
    return connect

@app.task
@database
def get_trade(k):
    """
    Get a submitted trade if it exists
    :param k: id of the item in the database
    :return: the processed data item as JSON or None
    """
    return r.db('cf').table('trades').get(k).run()

@app.task()
@database
def process_trade(k):
    """
    Process a submitted 'trade'
    :param k: id of the item in the database
    :return: the processed data item as JSON or False
    """
    trade = r.db('cf').table('trades').get(k).run()
    if trade:
        exists = r.db('cf').table('processed').get(k).run()
        if exists is None:
            data = r.db('cf').table('processed').insert(trade).run()
            return data
        else:
            return exists
    else:
        return False

if __name__ == '__main__':
    #celeryctl purge
    from celery.task.control import discard_all
    discard_all()
    print(process_trade('ca7a131b-6b8b-4541-a7e9-f4e1e6090400'))
