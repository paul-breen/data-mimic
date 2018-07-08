###############################################################################
# Project: Data Mimic
# Purpose: Class to load Mimics
# Author:  Paul M. Breen
# Date:    2018-06-24
###############################################################################

import importlib
import json

class Mimics(object):
    """
    Configure and load Mimics
    """

    def __init__(self, conf):
        """
        Constructor
        """

        self.mimics = {}
        self.conf = conf

    @staticmethod
    def get_configuration(conf_file):
        """
        Read the mimics JSON configuration file

        :param conf_file: The pathname of the configuration file
        :type conf_file: str
        :returns: The JSON configuration
        :rtype: dict
        """

        conf = {}

        with open(conf_file, 'r') as fp:
            conf = json.load(fp)

        return conf

    def init_mimics(self):
        """
        Initialise the mimics from the configuration
        """

        design_mode = self.conf['global']['design_mode']

        # Dynamically load, instantiate and initialise the mimic classes
        for item in self.conf['mimics']:
            m = importlib.import_module(item['module'])
            c = getattr(m, item['class'])
            o = c(item['id'])
            o.init(bg_image=item['bg_image'], objects=item['objects'], design_mode=design_mode)
            self.mimics.update({o.get_id(): o})

    def get_mimic(self, id):
        """
        Get the mimic for the given ID

        :param id: The ID of the mimic
        :type id: str
        :returns: The mimic
        :rtype: maplotlib object
        """

        return self.mimics[id]

