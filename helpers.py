import datetime
import json
from pathlib import Path
import sys


def _config(key):
    """ Return configuration values from the config.json file.

    Arguments:
    key {string} -- Name of the key in the config.json file.
    """

    my_file = Path('config.json')
    if not my_file.is_file():

        print('--- Main config.json file not found. Exiting.')

        sys.exit()

    config_file = open('config.json')
    config = config_file.read()

    if not config:

        print('--- config.json invalid. Exiting.')

        sys.exit()

    config = json.loads(config)

    if config.get(key):

        return config.get(key)

    else:

        print('--- config.json invalid. Exiting.')

        sys.exit()


def _info(message):
    """ Print info messages to the console.

    Arguments:
    message {string} -- Log message.
    """

    print(' _info > ' + message)


def _error(message):
    """ Print error messages to the console.

    Arguments:
    message {string} -- Log message.
    """

    print(' _error > ' + message)
