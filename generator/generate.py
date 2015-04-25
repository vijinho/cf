# -*- coding: utf8 -*-
"""
Generate some random data for the CF engineering challenge
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import codecs
import json
import random
import time
import functools

from builtins import *


__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"


def load_json(filename, key):
    with codecs.open(filename, 'r', 'utf8') as fh:
        objects = json.loads(fh.read())
    data = dict()
    for o in objects:
        data[o[key]] = o
    return data


def get_countries(filename='../data/countries.json', key='alpha2'):
    return load_json(filename, key)


def get_currencies(filename='../data/currencies.json', key='code'):
    return load_json(filename, key)


def get_languages(filename='../data/languages.json', key='alpha2'):
    return load_json(filename, key)


def get_regions(filename='../data/regions.json'):
    with codecs.open(filename, 'r', 'utf8') as fh:
        objects = json.loads(fh.read())
    data = dict()
    for region, country in dict.items(objects):
        data[region] = country
    return data

def get_rates(filename='../data/rates.json', key='year'):
    return load_json(filename, key)

def get_weighted_userid():
    x = 0
    n = random.randint(1,6)
    if n is 1:
        x = random.randint(1,3000)
    elif n is 2:
        x = random.randint(1,8000)
    elif n is 3:
        x = random.randint(1,17000)
    elif n is 4:
        x = random.randint(1,33000)
    elif n is 5:
        x = random.randint(1,48000)
    elif n is 6:
        x = random.randint(1,65000)
    return x

def random_weighted_country():
    n = random.randint(1,100)
    if n < 50:
        currency = 'EUR'
        # weigh the EURO country
        n = random.randint(1,100)
        if n <= 20:
            country = 'DE'
        elif n > 20 and n <= 45:
            country = 'FR'
        elif n > 45 and n <= 65:
            country = 'IT'
        elif n > 65 and n <= 80:
            country = 'ES'
        elif n > 80 and n < 85:
            country = 'NL'
        else:
            country = "".join(random.sample(eurozone,1))
    elif n > 50 and n <= 70:
        country = 'US'
    elif n > 70 and n <= 80:
        country = 'AU'
    elif n > 80 and n <= 90:
        n = random.randint(1,4)
        if n is 1:
            country = 'BR'
        elif n is 2:
            country = 'RU'
        elif n is 3:
            country = 'IN'
        elif n is 4:
            country = 'CN'
    else:
        country = "".join(random.sample(countries.keys(),1))
    return country

def random_weighted_currency():
    # choose currency by share of world trade
    n = random.randint(1,100)
    if n <= 27:
        currency = 'EUR'
    elif n > 27 and n <= 42:
        currency = 'USD'
    elif n > 42 and n <= 47:
        currency = 'JPY'
    elif n > 47 and n <= 51:
        currency = 'GBP'
    elif n > 51 and n <= 63:
        currency = 'CNY'
    elif n > 63 and n <= 65:
        currency = 'RUB'
    elif n > 65 and n <= 68:
        currency = 'MXN'
    elif n > 68 and n <= 71:
        currency = 'HKD'
    elif n > 71 and n <= 74:
        currency = 'CAD'
    elif n > 75 and n <= 77:
        currency = 'SGD'
    elif n > 78 and n <= 83:
        currency = 'AUD'
    elif n is 84:
        currency = 'SEK'
    elif n is 85:
        currency = 'CHF'
    elif n is 86:
        currency = 'THB'
    elif n is 87:
        currency = 'NOK'
    else:
        currency = "".join(random.sample(currencies.keys(),1))

    if (currency not in accepted_currencies):
        return random_weighted_currency()

    return currency

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start=None, end=None, prop=None, format='%d%b%y %H:%M:%S'):
    if start is None:
        t = time.gmtime()
        start = time.strftime(format, t)
    if end is None:
        t = time.gmtime()
        end = time.strftime(format, t)
    if prop is None:
        prop = random.random()
    return str_time_prop(start, end, format, prop).upper()

def random_weighted_date():
    n = random.randint(0,100)
    if n <= 25:
        dateFrom = "01JAN15 00:00:00"
        dateTo = None
    elif n > 25 and n <= 45:
        dateFrom = "01JAN14 00:00:00"
        dateTo = "01JAN15 00:00:00"
    elif n > 45 and n <= 63:
        dateFrom = "01JAN13 00:00:00"
        dateTo = "01JAN14 00:00:00"
    elif n > 63 and n <= 85:
        dateFrom = "01JAN12 00:00:00"
        dateTo = "01JAN13 00:00:00"
    elif n > 85 and n <= 95:
        dateFrom = "01JAN11 00:00:00"
        dateTo = "01JAN12 00:00:00"
    elif n > 95:
        dateFrom = "01MAY10 00:00:00"
        dateTo = "01JAN11 00:00:00"
    return random_date(dateFrom,dateTo)

def random_amount():
    n = random.randint(0,100)
    x = 0
    y = 0
    if n <= 5:
        x = 1000
        y = 300
    elif n > 10 and n <= 25:
        x = 5000
        y = 1500
    elif n > 25 and n <= 50:
        x = 25000
        y = 10000
    elif n > 50 and n <= 70:
        x = 30000
        y = 20000
    elif n > 70 and n <= 85:
        x = 500000
        y = 300000
    elif n > 85 and n <= 95:
        x = 1000000
        y = 4000000
    elif n > 95 and n <= 97:
        x = 5000000
        y = 3000000
    elif n > 97 and n <= 100:
        x = 50000000
        y = 30000000
    return abs(random.gauss(x,y))

def generate_trade(dateFrom=None,dateTo=None):
    trade = dict()
    trade['userId'] = get_weighted_userid()

    # weight the date
    if dateFrom is None and dateTo is None:
        timePlaced = random_weighted_date()
    else:
        timePlaced = random_date(dateFrom,dateTo)
    trade['timePlaced'] = timePlaced

    currencyTo = False
    currencyFrom = False
    while currencyFrom is False or currencyFrom is currencyTo:
        originatingCountry = random_weighted_country()
        country = countries[originatingCountry]

        # lets assume 10% of transfers are in a currency different from that of originatingCountry
        if random.randint(1,10) > 1:
            # some countries have 0 or more than 1 currency
            ccurrencies = country['currencies']
            x = len(ccurrencies)
            if x is 0:
                currencyFrom = False
            if x is 1:
                currencyFrom = ccurrencies[0]
            elif x > 1:
                currencyFrom = "".join(random.sample(accepted_currencies,1))
        else:
            currencyFrom = random_weighted_currency()

    trade['originatingCountry'] = originatingCountry
    trade['currencyFrom'] = currencyFrom

    currencyTo = currencyFrom
    while currencyTo is currencyFrom:
        currencyTo = random_weighted_currency()
    trade['currencyTo'] = currencyTo

    amountSell = random_amount()

    trade['amountSell'] = float(round(amountSell, currencies[currencyFrom]['decimals']))

    return trade

def setup_global_data():
    global countries, currencies, languages, regions, eurozone, rates, accepted_currencies
    countries = get_countries()
    currencies = get_currencies()
    languages = get_languages()
    regions = get_regions()
    eurozone = regions['eurozone']
    rates = get_rates()
    accepted_currencies = list(rates['2015']['rates'].keys())

if __name__ in '__main__':
    setup_global_data()
    print(generate_trade())
