#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

from feeder import daemon
import os

environments = {
    'production' : {
        'number': '34644298488',
        'password': 'iggEzRpQKOA16GvCCPDF6n6qX4A='
    },
    'development': {
        'number': '34670712480',
        'password': '3rRu6WJKA6jyLIwpa+FVYWAElzc='
    }
    }
env = os.getenv('WENV') or 'development'
config = environments[env]
daemon.run(config['number'], config['password'])
