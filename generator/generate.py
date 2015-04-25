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


def random_date(start=None, end=None, prop=None, format='%d-%b-%y %H:%M:%S'):
    if start is None:
        t = time.gmtime()
        start = time.strftime(format, t)
    if end is None:
        t = time.gmtime()
        end = time.strftime(format, t)
    if prop is None:
        prop = random.random()
    d = str_time_prop(start, end, format, prop).upper()
    if random.randint(1,10) <= 7:
        min = 8
        max = 18
    else:
        min = 0
        max = 23
    d = "".join([d[0:10],"{hour:02d}:{min:02d}:{sec:02d}".format(
            hour=random.randint(min,max),
            min=random.randint(0,59),
            sec=random.randint(0,59)
        )])
    return d

def random_weighted_date():
    n = random.randint(0,100)
    if n <= 25:
        dateFrom = "01-JAN-15 00:00:00"
        dateTo = None
    elif n > 25 and n <= 45:
        dateFrom = "01-JAN-14 00:00:00"
        dateTo = "01-JAN-15 00:00:00"
    elif n > 45 and n <= 63:
        dateFrom = "01-JAN-13 00:00:00"
        dateTo = "01-JAN-14 00:00:00"
    elif n > 63 and n <= 85:
        dateFrom = "01-JAN-12 00:00:00"
        dateTo = "01-JAN-13 00:00:00"
    elif n > 85 and n <= 95:
        dateFrom = "01-JAN-11 00:00:00"
        dateTo = "01-JAN-12 00:00:00"
    elif n > 95:
        dateFrom = "01-MAY-10 00:00:00"
        dateTo = "01-JAN-11 00:00:00"
    return random_date(dateFrom,dateTo)

def random_amount():
    n = random.randint(0,10000)
    x = 0
    y = 0
    if n <= 5000:
        x = random.randint(1,3) * 500
    elif n > 5000 and n <= 6500:
        x = random.randint(1,5) * 1000
    elif n > 6500 and n <= 8000:
        x = random.randint(1,2) * 5000
    elif n > 8000 and n <= 8500:
        x = random.randint(1,3) * 250
    elif n > 8500 and n <= 9950:
        x = random.randint(1,3) * 500
    elif n > 9950 and n <= 9990:
        x = random.randint(1,5) * 5000
    elif n > 9990 and n <= 9995:
        x = random.randint(1,5) * 50000
    elif n > 9995 and n <= 9999:
        x = random.randint(1,5) * 100000
    elif n > 9999 and n <= 10000:
        x = random.randint(1,5) * 1000000
    return round(abs(random.gauss(x,x/5)))

def generate_trade(dateFrom=None,dateTo=None,live=False,today=False,return_json=False):
    trade = dict()
    trade['userId'] = get_weighted_userid()

    if live is True or today is True:
        t = time.gmtime()
        format='%d-%b-%y %H:%M:%S'
        dateFrom = time.strftime(format, t)
        if live is True:
            timePlaced = dateFrom
        else:
            timePlaced = random_date()
    else:
        # weight the date
        if dateFrom is None and dateTo is None:
            timePlaced = random_weighted_date()
        else:
            timePlaced = random_date(dateFrom,dateTo)

    trade['timePlaced'] = timePlaced
    year_rates = rates['20' + trade['timePlaced'][7:9]]['rates']

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
    while currencyTo == currencyFrom:
        currencyTo = random_weighted_currency()
    trade['currencyTo'] = currencyTo

    amountSell = random_amount()
    try:
        if currencyFrom == 'EUR':
            eurAmount = amountSell
            rate = year_rates[currencyTo]
            rate = abs(random.gauss(rate,0.02))
            amountBuy = eurAmount * rate
        else:
            eurAmount = amountSell / year_rates[currencyFrom]
            amountBuy = eurAmount * year_rates[currencyTo]
            rate = amountBuy / eurAmount
            rate = abs(random.gauss(rate,0.02))
    except Exception:
        return generate_trade(dateFrom=dateFrom,dateTo=dateTo,live=live,today=today,return_json=return_json)

    trade['rate'] = round(rate,5)
    trade['amountSell'] = float(round(amountSell, currencies[currencyFrom]['decimals']))
    trade['amountBuy'] = float(round(amountBuy, currencies[currencyTo]['decimals']))
    trade['amountBuyEur'] = float(round(eurAmount, currencies[currencyTo]['decimals']))

    if return_json is True:
        return json.dumps(trade, indent=4, sort_keys=True)
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

def generate_trades_to_sum(max=50000000,dateFrom=None,dateTo=None,today=False,live=False,return_json=True):
    trades = list()
    total = 0
    i = 0
    max = abs(random.gauss(max,max/4.5))

    while total < max:
        trade = generate_trade(dateFrom=dateFrom,dateTo=dateTo,live=live,today=today)
        total = total + trade['amountBuyEur']
        del trade['amountBuyEur']
        i = i + 1
        trades.append(trade)

    if return_json is True:
        return json.dumps(trades, indent=4, sort_keys=True)
    else:
        return trades

if __name__ in '__main__':
    setup_global_data()
    trades = generate_trades_to_sum(10000000,live=False,today=True)
    print(trades)
    print(generate_trade(return_json=True,live=True))
