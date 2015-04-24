#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))

import os

from service import daemon

environments = {
    'production' : {
        'number': '',
        'password': ''
    },
    'development': {
        'number': '14153479219',
        'password': 'rnYDbiM3ZXw917CMSwY+xPOgT6A='
    }
    }
env = os.getenv('WENV') or 'development'
config = environments[env]
daemon.run(config['number'], config['password'])
