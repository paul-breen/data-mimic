###############################################################################
# Project: Data Mimic
# Purpose: Module to encapsulate the datamimic application functionality
# Author:  Paul M. Breen
# Date:    2018-06-24
###############################################################################

# It is crucial that we do this as early as possible, to turn off the Tkinter
# interface of matplotlib.  We don't require it, as we're using matplotlib
# in a web application
import matplotlib
matplotlib.use('agg')

from datamimic.Mimics import Mimics

import click
from flask import Flask
from flask import request
from flask.cli import AppGroup
from flask_dotenv import DotEnv
from flask_cors import CORS
import mpld3
import json

app = Flask(__name__)
env = DotEnv(app)
CORS(app)

# Find the path to the mimics configuration from a .env file
try:
    conf_file = app.config['MIMICS_CONF']
except KeyError:
    conf_file = 'mimics.json'

# Load, instantiate and initialise the mimics
conf = Mimics.get_configuration(conf_file)
mimics = Mimics(conf)
mimics.init_mimics()

# Mimic commands
mimic_cli = AppGroup('mimic', help='Data Mimic commands')

@mimic_cli.command('update', help='Update the given mimic')
@click.argument('id')
@app.route('/mimic/update/<id>')
def mimic_update(id):
    """
    Update the mimic for the given ID

    :param id: The ID of the mimic
    :type id: int
    :returns: The mimic
    :rtype: maplotlib object
    """

    content_type = request.args.get('content_type', default='html', type=str)

    mimic = mimics.get_mimic(id)

    # N.B.: This doesn't serialize to JSON at the moment.  Is it because we're
    #       using a static image as the background?
    if content_type == 'json':
        return json.dumps(mpld3.fig_to_dict(mimic.update()))
    else:
        return mpld3.fig_to_html(mimic.update())

app.cli.add_command(mimic_cli)

