# -*- coding: utf8 -*-
"""
Consume POSTed messages for trades
"""

import json

from builtins import *
import falcon
import rethinkdb as r

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
            req.context['code'] = 0
            req.context['msg'] = 'OK'
            req.context['data'] = {}
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

        msg = req.context['msg']
        code = int(req.context['code'])
        if code != 0:
            msg = "Error: {msg}".format(msg=msg)

        ret['msg'] = msg
        ret['code'] = code
        ret['data'] = req.context['data']

        resp.body = json.dumps(str(ret).encode('utf8'), indent=4,
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
        return True

    @falcon.before(max_body(256 * 1024))
    def on_post(self, req, resp):
        try:
            items = req.context['json']
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        if self.validate(req, resp, items):
            data = list()
            for o in items:
                data.append(o)
            # r.connect('localhost', 28015).repl()
            # data = r.db('cf').table('trades').count().run()
            req.context['data'] = data


app = falcon.API(middleware=[
    JsonRequire(),
    JsonDecode(),
])
trade = AcceptTrade()
app.add_route('/trade', trade)

if __name__ == '__main__':
    print("Start from top-level with bin/startconsumer.sh")
