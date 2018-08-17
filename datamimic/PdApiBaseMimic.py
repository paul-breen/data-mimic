###############################################################################
# Project: Data Mimic
# Purpose: Base class to encapsulate default PLC Data API mimic behaviour
# Author:  Paul M. Breen
# Date:    2018-08-17
###############################################################################

import requests

from datamimic.BaseMimic import BaseMimic

class PdApiBaseMimic(BaseMimic):
    DEFAULTS = {
        'conf': {
            'url': 'http://localhost:5000',
            'routes': {
                'data': '/get_value/',
                'metadata': '/get_metric/'
            }
        }
    }
 
    def __init__(self, id, conf={}):
        super().__init__(id)
        self.conf = self.DEFAULTS['conf']
        self.conf.update(conf)
        self.base_url = self.conf['url']

    def get_variable(self, name):
        url = self.base_url + self.conf['routes']['data'] + name

        response = requests.get(url)
        d = response.json()

        if not d['success']:
            raise ValueError("Failed to get PLC Data API tag {} value".format(name))
        else:
            value = d['data']['value']

        return value

