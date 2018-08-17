###############################################################################
# Project: Data Mimic
# Purpose: Class to load Mimics
# Author:  Paul M. Breen
# Date:    2018-06-24
###############################################################################

import importlib
import json
import re

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

    @staticmethod
    def construct_mimic_title(id):
        """
        Construct the mimic title for the given ID

        :param id: The ID of the mimic
        :type id: str
        :returns: The mimic title
        :rtype: str
        """

        return re.sub('[_-]', ' ', id).title()

    def get_item_conf(self, item):
        """
        Get the mimic item's optional configuration property
        """

        conf = {}

        try:
            conf = item['conf']
        except KeyError:
            pass

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
            o = c(item['id'], conf=self.get_item_conf(item))
            o.init(figsize=item['figsize'], bg_image=item['bg_image'], objects=item['objects'], design_mode=design_mode)
            o.title = Mimics.construct_mimic_title(item['id'])
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

    def get_mimic_list(self):
        """
        Get a list of all available mimics

        :returns: A list of available mimics
        :rtype: list
        """
     
        mimic_list = []

        for id in self.mimics:
            m = self.get_mimic(id)
            d = {
                'id': id,
                'title': m.title,
                'objects': m.objects,
                'variables': m.variables
            }
            mimic_list.append(d)

        return mimic_list

