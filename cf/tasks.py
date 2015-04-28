# -*- coding: utf8 -*-
"""
Process trades
"""
import os
import json
import time
from celery import Celery
import rethinkdb as r
import generate as g
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

@app.task(default_retry_delay=300, max_retries=6)
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
            # create timestamp field (YYYY-MM-DD HH:MM:SS)
            time_placed = trade['timePlaced']
            ts_format='%d-%b-%y %H:%M:%S'
            t = time.mktime(time.strptime(time_placed, ts_format))
            trade['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
            trade['unixtime'] = time.strftime("%s", time.localtime(t))

            # calculate the trade amount bought in euros
            if 'EUR' in trade['currencyFrom']:
                amount_buy = trade['currencyFrom']
            elif 'EUR' in trade['currencyTo']:
                amount_buy = trade['currencyTo']
            else:
                year_rates = g.rates['20' + trade['timePlaced'][7:9]]['rates']
                eur_amount = trade['amountSell'] / year_rates[trade['currencyFrom']]
                amount_buy = eur_amount * year_rates[trade['currencyTo']]
                amount_buy = round(eur_amount, g.currencies[trade['currencyTo']]['decimals'])
            trade['amountEur'] = amount_buy
            trade['currencyPair'] = "{0}/{1}".format(trade['currencyFrom'],trade['currencyTo'])
            trade['originatingCountryName'] = g.countries[trade['originatingCountry']]['name']

            data = r.db('cf').table('processed').insert(trade).run()
            return data
        else:
            return True
    else:
        return False

if __name__ == '__main__':
    #celeryctl purge
    from celery.task.control import discard_all
    discard_all()
    print(process_trade('1e730047-520e-4c9b-a08e-d2fe7c9f198c'))
