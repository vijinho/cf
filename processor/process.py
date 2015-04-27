# -*- coding: utf8 -*-
"""
Process trades
"""

import json
import time
import rethinkdb as r
from generator import generate as g
from builtins import *

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"



if __name__ == '__main__':
    print("Start from top-level with bin/startprocessor.sh")
