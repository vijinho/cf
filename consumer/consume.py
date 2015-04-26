# -*- coding: utf8 -*-
"""
Consume POSTed messages for trades
"""

from builtins import *

import falcon

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"

class ConsumeResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = ("\nI've always been more interested in\n"
                     'the future than in the past.\n'
                     '\n'
                     '    ~ Grace Hopper\n\n')

app = falcon.API()
trade = ConsumeResource()
app.add_route('/trade', trade)

if __name__ == '__main__':
    print("Start with 'gunicorn consume:app'")
