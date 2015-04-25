# -*- coding: utf8 -*-
"""
Generate some random data for the CF engineering challenge
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import codecs
import json

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

def setup_global_data():
    global countries, currencies, languages, regions, eurozone
    countries = get_countries()
    currencies = get_currencies()
    languages = get_languages()
    regions = get_regions()
    eurozone = regions['eurozone']

if __name__ in '__main__':
    setup_global_data()
    print(countries['ES'])
