# -*- coding: utf8 -*-
"""
Generate some random data for the CF engineering challenge
"""
import codecs
import json
import random
import time
import click

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
    """
    Load in a JSON file and return it indexed by a key
    :param filename: json file to load
    :param key: index data with this attribute key
    :return: dict of objects indexed by key
    """
    with codecs.open(filename, 'r', 'utf8') as fh:
        objects = json.loads(fh.read())
    data = dict()
    for o in objects:
        data[o[key]] = o
    return data


def get_countries(filename='data/countries.json', key='alpha2'):
    return load_json(filename, key)


def get_currencies(filename='data/currencies.json', key='code'):
    return load_json(filename, key)


def get_languages(filename='data/languages.json', key='alpha2'):
    return load_json(filename, key)


def get_rates(filename='data/rates.json', key='year'):
    return load_json(filename, key)


def get_regions(filename='data/regions.json'):
    """
    Return groups of countries indexed by a region name
    :param filename:
    :return: dict of countries indexed by region name
    """
    with codecs.open(filename, 'r', 'utf8') as fh:
        objects = json.loads(fh.read())
    data = dict()
    for region, country in dict.items(objects):
        data[region] = country
    return data


def get_weighted_userid(year):
    """
    Get a user ID value weighted
    :return: uid in range for that year
    """
    if year == 2010:
        x = 5000
    elif year == 2011:
        x = 20000
    elif year == 2012:
        x = 30000
    elif year == 2013:
        x = 40000
    elif year == 2014:
        x = 50000
    elif year == 2015:
        x = 65000
    else:
        x = 100000

    return random.randint(1, x)


def random_weighted_country():
    """
    Return a random country, weighted by assumed frequency of trade
    :return: 2 char country code
    """
    n = random.randint(1, 100)
    if n < 50:
        # weigh the EURO country
        n = random.randint(1, 100)
        if n <= 20:
            country = 'DE'
        elif 20 < n <= 45:
            country = 'FR'
        elif 45 < n <= 65:
            country = 'IT'
        elif 65 < n <= 80:
            country = 'ES'
        elif 80 < n < 85:
            country = 'NL'
        else:
            country = "".join(random.sample(eurozone, 1))
    elif 50 < n <= 70:
        country = 'US'
    elif 70 < n <= 80:
        country = 'AU'
    elif 80 < n <= 90:
        n = random.randint(1, 4)
        if n is 1:
            country = 'BR'
        elif n is 2:
            country = 'RU'
        elif n is 3:
            country = 'IN'
        elif n is 4:
            country = 'CN'
    else:
        country = "".join(random.sample(countries.keys(), 1))
    return country


def random_weighted_currency():
    """
    Return a random accepted currency weighted by importance in trade frequency
    :return: 3 char currency code
    """
    # choose currency by share of world trade
    n = random.randint(1, 100)
    if n <= 27:
        currency = 'EUR'
    elif 27 < n <= 42:
        currency = 'USD'
    elif 42 < n <= 47:
        currency = 'JPY'
    elif 47 < n <= 51:
        currency = 'GBP'
    elif 51 < n <= 63:
        currency = 'CNY'
    elif 63 < n <= 65:
        currency = 'RUB'
    elif 65 < n <= 68:
        currency = 'MXN'
    elif 68 < n <= 71:
        currency = 'HKD'
    elif 71 < n <= 74:
        currency = 'CAD'
    elif 75 < n <= 77:
        currency = 'SGD'
    elif 78 < n <= 83:
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
        currency = "".join(random.sample(currencies.keys(), 1))

    if currency not in accepted_currencies:
        return random_weighted_currency()

    return currency


def str_time_prop(start, end, ts_format, prop):
    """
    format a date time string
    :param start: timestamp
    :param end: timestamp
    :param ts_format: format for timestamp
    :param prop: time difference range
    :return:
    """
    start_time = time.mktime(time.strptime(start, ts_format))
    end_time = time.mktime(time.strptime(end, ts_format))
    ptime = start_time + prop * (end_time - start_time)
    return time.strftime(ts_format, time.localtime(ptime))


def random_date(start=None, end=None, prop=None, ts_format='%d-%b-%y %H:%M:%S'):
    """
    Return a random date/time timestamp, weighted by EU office hours for larger frequency of trades
    :param start:
    :param end:
    :param prop:
    :param ts_format:
    :return:
    """
    if start is None:
        t = time.gmtime()
        start = time.strftime(ts_format, t)
    if end is None:
        t = time.gmtime()
        end = time.strftime(ts_format, t)
    if prop is None:
        prop = random.random()
    d = str_time_prop(start, end, ts_format, prop)
    if random.randint(1, 10) <= 7:
        min_hr = 8
        max_hr = 18
    else:
        min_hr = 0
        max_hr = 23
    d = "".join([d[0:10], "{hour:02d}:{min:02d}:{sec:02d}".format(
        hour=random.randint(min_hr, max_hr),
        min=random.randint(0, 59),
        sec=random.randint(0, 59)
    )])
    return d.upper()


def random_weighted_date():
    """
    Return a random date from the sdate of the first trade in the system to the present day
    :return: formatted timestamp
    """
    n = random.randint(0, 100)
    if n <= 25:
        date_from = "01-JAN-15 00:00:00"
        date_to = None
    elif 25 < n <= 45:
        date_from = "01-JAN-14 00:00:00"
        date_to = "01-JAN-15 00:00:00"
    elif 45 < n <= 63:
        date_from = "01-JAN-13 00:00:00"
        date_to = "01-JAN-14 00:00:00"
    elif 63 < n <= 85:
        date_from = "01-JAN-12 00:00:00"
        date_to = "01-JAN-13 00:00:00"
    elif 85 < n <= 95:
        date_from = "01-JAN-11 00:00:00"
        date_to = "01-JAN-12 00:00:00"
    elif n > 95:
        date_from = "01-MAY-10 00:00:00"
        date_to = "01-JAN-11 00:00:00"
    return random_date(date_from, date_to)


def random_amount():
    """
    Get a weighted random amount for a currency transfer
    :return: currency amount
    """
    n = random.randint(0, 10000)
    x = 0
    if n <= 5000:
        x = random.randint(1, 3) * 500
    elif 5000 < n <= 6500:
        x = random.randint(1, 5) * 1000
    elif 6500 < n <= 8000:
        x = random.randint(1, 2) * 5000
    elif 8000 < n <= 8500:
        x = random.randint(1, 3) * 250
    elif 8500 < n <= 9950:
        x = random.randint(1, 3) * 500
    elif 9950 < n <= 9990:
        x = random.randint(1, 5) * 5000
    elif 9990 < n <= 9995:
        x = random.randint(1, 5) * 50000
    elif 9995 < n <= 9999:
        x = random.randint(1, 5) * 100000
    elif 9999 < n <= 10000:
        x = random.randint(1, 5) * 1000000
    return round(abs(random.gauss(x, x / 5)))


def generate_trade(date_from=None, date_to=None, live=False, today=False,
                   return_json=False):
    """
    Generate a random trade
    :param date_from: the date range start point timestamp
    :param date_to: the date range end point timestamp
    :param live: create a live trade from this moment
    :param today: create a trade that was made at some point today
    :param return_json: return the trade as json
    :return:
    """
    trade = dict()

    if live is True or today is True:
        t = time.gmtime()
        ts_format = '%d-%b-%y %H:%M:%S'
        date_from = time.strftime(ts_format, t)
        if live is True:
            time_placed = date_from
        else:
            time_placed = random_date()
    else:
        # weight the date
        if date_from is None and date_to is None:
            time_placed = random_weighted_date()
        else:
            time_placed = random_date(date_from, date_to)

    trade['timePlaced'] = time_placed.upper()
    year_rates = rates['20' + trade['timePlaced'][7:9]]['rates']

    currency_to = False
    currency_from = False
    while currency_from is False or currency_from is currency_to:
        originating_country = random_weighted_country()
        country = countries[originating_country]

        # lets assume 10% of transfers are in a currency different
        # from that of originating_country
        if random.randint(1, 10) > 1:
            # some countries have 0 or more than 1 currency
            ccurrencies = country['currencies']
            x = len(ccurrencies)
            if x is 0:
                currency_from = False
            if x is 1:
                currency_from = ccurrencies[0]
            elif x > 1:
                currency_from = "".join(random.sample(accepted_currencies, 1))
        else:
            currency_from = random_weighted_currency()

    trade['originatingCountry'] = originating_country
    trade['currencyFrom'] = currency_from

    currency_to = currency_from
    while currency_to == currency_from:
        currency_to = random_weighted_currency()
    trade['currencyTo'] = currency_to

    amount_sell = random_amount()
    if currency_from == 'EUR':
        eur_amount = amount_sell
        if not currency_from in year_rates or not currency_to in year_rates:
            return generate_trade(date_from=date_from, date_to=date_to,
                                  live=live,
                                  today=today, return_json=return_json)
        rate = year_rates[currency_to]
        rate = abs(random.gauss(rate, 0.02))
        amount_buy = eur_amount * rate
    else:
        if not currency_from in year_rates or not currency_to in year_rates:
            return generate_trade(date_from=date_from, date_to=date_to,
                                  live=live,
                                  today=today, return_json=return_json)
        eur_amount = amount_sell / year_rates[currency_from]
        amount_buy = eur_amount * year_rates[currency_to]
        rate = amount_buy / eur_amount
        rate = abs(random.gauss(rate, 0.02))

    trade['rate'] = round(rate, 5)
    trade['amountSell'] = float(
        round(amount_sell, currencies[currency_from]['decimals']))
    trade['amountBuy'] = float(
        round(amount_buy, currencies[currency_to]['decimals']))
    trade['amountBuyEur'] = float(
        round(eur_amount, currencies[currency_to]['decimals']))

    trade['userId'] = get_weighted_userid(int("20" + str(trade['timePlaced'][7:9])))

    if return_json is True:
        del trade['amountBuyEur']
        return json.dumps(trade, indent=4, sort_keys=True)
    return trade


def generate_trades_to_sum(max_sum=50000000, date_from=None, date_to=None,
                           today=False, live=False, return_json=True):
    """
    Generate a list of trades
    :param max_sum: the approx maximum total value of all trades
    :param date_from: the date range start timestamp
    :param date_to: the date tange end timestamp
    :param today: get a list of random trades for this day
    :param live: get a list of randoom trades for this point in time
    :param return_json: return data as json
    :return:
    """
    trades_list = list()
    total = 0
    i = 0
    max_sum = abs(random.gauss(max_sum, max_sum / 4.5))

    while total < max_sum:
        trade = generate_trade(date_from=date_from, date_to=date_to, live=live,
                               today=today)
        total = total + trade['amountBuyEur']
        del trade['amountBuyEur']
        i += 1
        trades_list.append(trade)

    if return_json is True:
        return json.dumps(trades_list, indent=4, sort_keys=True)
    else:
        return trades_list


def setup_global_data():
    """
    setup some global variables used by the rest of the functions
    :return:
    """
    global countries, currencies, languages, regions, eurozone
    global rates, accepted_currencies
    countries = get_countries()
    currencies = get_currencies()
    languages = get_languages()
    regions = get_regions()
    eurozone = regions['eurozone']
    rates = get_rates()
    accepted_currencies = list(rates['2015']['rates'].keys())

setup_global_data()

@click.command()
@click.option('--live', '-l', is_flag=True, default=False, help="Simulate a live trade?")
@click.option('--today', '-t', is_flag=True, default=False, help="Simulate a trade made today?")
@click.option('--historic', '-h', is_flag=True, default=False, help="Simulate historic data?")
@click.option('--quantity', '-q', default=1, help="Exact number of trades to generate?")
@click.option('--amount', '-a', default=0, help="Generate a random number of trades totalling APPROX this amount equivalent in EUR")
@click.option('--datestart', '-s', default=None, help='Enter date range start: format "01-JAN-2015 00:00:00"')
@click.option('--dateend', '-e', default=None, help='Enter date range end: format "01-JAN-2015 00:00:00"')
@click.option('--csv', '-c', is_flag=True, default=False, help="Output CSV instead of JSON?")
@click.option('--outfile', '-f', default=None, help='Filename to output results.')
@click.option('-v', '--verbose', count=True)
def generate(live,today,historic,quantity,amount,datestart,dateend,csv,outfile,verbose):
    if today is True:
        historic = False
    if live is True:
        historic = False
        today = False
    if historic is True:
        today = False
        live = False

    if amount == 0:
        trades_list = list()
        for i in range(0,quantity):
            trade = generate_trade(return_json=True,live=live,today=today,date_from=datestart,date_to=dateend)
            trades_list.append(trade)
        data = json.dumps(trades_list, indent=4, sort_keys=True)
    else:
        data = generate_trades_to_sum(return_json=True,live=live,today=today,max_sum=amount,date_from=datestart,date_to=dateend)

    if outfile:
        with open(outfile, 'wb') as fh:
            fh.write(str(data).encode('utf8'))
    else:
        print(data)

if __name__ == '__main__':
    generate()
    #    pass
#    trades = generate_trades_to_sum(10000000, live=False, today=False)
#    print(trades)
#    print(generate_trade(return_json=True, live=True))
