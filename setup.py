###############################################################################
# Project: Data Mimic
# Purpose: Packaging configuration for the Data Mimic project
# Author:  Paul M. Breen
# Date:    2018-07-31
###############################################################################

from setuptools import setup

setup(name='data-mimic',
      version='0.1',
      description='Data Mimic',
      url='https://github.com/paul-breen/data-mimic',
      author='Paul Breen',
      author_email='paul.breen6@btinternet.com',
      license='Apache 2.0',
      packages=['datamimic'],
      package_data={'datamimic': [
          'examples/dummy-data/*',
          'examples/dummy-data/images/*',
          'examples/dummy-data/mimics/*',
          'examples/pds/*',
          'examples/pds/images/*',
          'examples/pds/mimics/*'
      ]},
      install_requires=[
          'click',
          'Flask',
          'Flask-Cors',
          'Flask-DotEnv',
          'matplotlib',
          'mpld3',
          'numpy',
          'pds',
          'Pillow',
          'python-dotenv'
      ])
