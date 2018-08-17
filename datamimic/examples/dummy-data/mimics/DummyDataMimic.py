###############################################################################
# Project: Data Mimic
# Purpose: Example derived mimic class
# Author:  Paul M. Breen
# Date:    2018-07-07
###############################################################################

import random

from datamimic.BaseMimic import BaseMimic

class DummyDataMimic(BaseMimic):
    def __init__(self, id, conf={}):
        super().__init__(id, conf=conf)
        self.dummy_data = {}

    def init(self, **kwargs):
        super().init(**kwargs)

        self.dummy_data = {
            'day_tank_status': lambda: random.randint(0, 2),
            'engine_status': lambda:  random.randint(0, 2),
            'engine_control_panel_active': lambda:  random.randint(0, 2),
            'day_tank_level': lambda : random.randint(1, 101)
        }

    def get_variable(self, name):
        return self.dummy_data[name]()

