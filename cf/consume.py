# -*- coding: utf8 -*-
"""
Consume POSTed messages for trades
"""

import json
import falcon
import time
import datetime as dt
import rethinkdb as r
from celery import Celery
from cf import generate as g
from cf import tasks as t
from builtins import *

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"


class JsonRequire(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JsonDecode(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        try:
            req.context['json'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        """Return encoded JSON with code and msg keys"""
        if 'data' not in req.context:
            return

        ret = dict()

        if 'msg' in req.context:
            msg = req.context['msg']
            if msg is None:
                msg = 'OK'
        else:
            msg = 'OK'
        ret['msg'] = msg

        if 'code' in req.context:
            code = int(req.context['code'])
            if code is None:
                code = 0
            elif code < 0:
                msg = "Error: {msg}".format(msg=msg)
        else:
            code = 0
        ret['code'] = code

        if 'data' in req.context:
            data = req.context['data']
            if data is None:
                data = {}
            req.context['data']
        else:
            data = {}
        ret['data'] = req.context['data']

        resp.body = json.dumps(ret, indent=4,
                               sort_keys=True)


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')
            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


class AcceptTrade:
    @staticmethod
    def validate(req, resp, items):
        required = ['userId',
                    'currencyFrom',
                    'currencyTo',
                    'amountSell',
                    'amountBuy',
                    'rate',
                    'timePlaced',
                    'originatingCountry']

        for o in items:
            fields = o.keys()
            for f in required:
                if f not in fields:
                    req.context['code'] = -1
                    req.context['msg'] = \
                        "Missing required keys for trade. Should include: ({keys})".\
                            format(keys=",".join(required))
                    return False

            if int(o['userId']) < 1:
                req.context['code'] = -2
                req.context['msg'] = "Bad userId encountered. Should be: positive INT"
                return False

            if float(o['amountSell']) < 1:
                req.context['code'] = -3
                req.context['msg'] = "Bad amountSell encountered. Should be: positive FLOAT"
                return False

            if float(o['amountBuy']) <= 0:
                req.context['code'] = -4
                req.context['msg'] = "Bad amountBuy encountered. Should be: positive FLOAT"
                return False

            if float(o['rate']) <= 0:
                req.context['code'] = -5
                req.context['msg'] = "Bad rate encountered. Should be: positive FLOAT"
                return False

            if len(o['currencyFrom']) != 3:
                req.context['code'] = -6
                req.context['msg'] = "Bad currencyFrom encountered. Should be: format XXX"
                return False

            if len(o['currencyTo']) != 3:
                req.context['code'] = -7
                req.context['msg'] = "Bad currencyTo encountered. Should be: format XXX"
                return False

            if o['currencyFrom'] == o['currencyTo']:
                req.context['code'] = -13
                req.context['msg'] = "currencyTo cannot be the same as currencyFrom! They should be different!"
                return False

            if len(o['originatingCountry']) != 2:
                req.context['code'] = -8
                req.context['msg'] = "Bad country encountered. Should be: format XX"
                return False

            if o['originatingCountry'] not in g.countries:
                req.context['code'] = -9
                req.context['msg'] = req.context['msg'] = \
                        "Invalid country encountered. Should be one of: ({keys})".\
                            format(keys=",".join(g.countries))
                return False

            if o['currencyFrom'] not in g.get_currencies():
                req.context['code'] = -10
                req.context['msg'] = req.context['msg'] = \
                        "Invalid currencyFrom encountered. Should be one of: ({keys})".\
                            format(keys=",".join(g.accepted_currencies))
                return False

            if o['currencyTo'] not in g.accepted_currencies:
                req.context['code'] = -11
                req.context['msg'] = req.context['msg'] = \
                        "Invalid currencyTo encountered. Should be one of: ({keys})".\
                            format(keys=",".join(g.accepted_currencies))
                return False

            try:
                d = time.mktime(time.strptime(o['timePlaced'], '%d-%b-%y %H:%M:%S'))
            except Exception :
                req.context['code'] = -12
                req.context['msg'] = "Invalid timePlaced value encountered. Should be in: format '06-MAY-76 07:30:00'"
                return False

        return True

    @falcon.before(max_body(256 * 1024))
    def on_post(self, req, resp):
        try:
            items = req.context['json']
            # if we are dealing with a single trade object, put it in a list
            if not isinstance(items, (list)):
                items = [items]
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        if self.validate(req, resp, items):
            r.connect('localhost', 28015).repl()
            data = r.db('cf').table('trades').insert(items).run()
            if 'generated_keys' in data:
                # send inserted trades to the processor,
                for k in data['generated_keys']:
                    print(k)
                    # start tasks in 30 seconds, expire in 10 mins from NOW
                    t.process_trade.apply_async(args=[k], countdown=30, expires=dt.datetime.now() + dt.timedelta(minutes=10))

            req.context['data'] = data

    @falcon.before(max_body(0))
    def on_get(self, req, resp):
        k = req.get_param('id', False)
        req.context['data'] = {}
        if (k):
            r.connect('localhost', 28015).repl()
#            r.db('cf').table('processed').get(k).delete().run()
            processed = r.db('cf').table('processed').get(k).run()
            if processed:
                req.context['data'] = processed
            else:
                trade = r.db('cf').table('trades').get(k).run()
                req.context['data'] = trade
                if trade:
                    req.context['msg'] = "Trade not processed yet. Resent for processing."
                    req.context['code'] = 1
                    t.process_trade.apply_async(args=[k], countdown=30, expires=dt.datetime.now() + dt.timedelta(minutes=10))
                else:
                    req.context['msg'] = "Trade not found."
                    req.context['code'] = -14

        else:
            req.context['msg'] = "Missing GET query param: id"
            req.context['code'] = -13
#            r.connect('localhost', 28015).repl()
#            req.context['data'] = r.db('cf').table('trades').run()

    @falcon.before(max_body(0))
    def on_delete(self, req, resp):
        k = req.get_param('id', False)
        req.context['data'] = {}
        if (k):
            r.connect('localhost', 28015).repl()
            r.db('cf').table('trades').get(k).delete().run()
            r.db('cf').table('processed').get(k).delete().run()
            req.context['msg'] = "Trade deleted"
        else:
            req.context['msg'] = "Missing GET query param: id"
            req.context['code'] = -14

app = falcon.API(middleware=[
    JsonRequire(),
    JsonDecode(),
])
trade = AcceptTrade()
app.add_route('/trade', trade)

if __name__ == '__main__':
    print("Start from top-level with bin/startconsumer.sh")
