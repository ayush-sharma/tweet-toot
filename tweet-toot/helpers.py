#!/usr/bin/env python3

import datetime
import json
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def _config(key):
    """ Return configuration values from the config.json file or the environment.

    Arguments:
    key {string} -- Name of the config key.
    """

    if key in os.environ:

        return os.environ[key]

    my_file = _read_file("config.json")
    if not my_file:

        logger.critical("Main config.json file not found. Exiting.")
        sys.exit()

    try:

        config = json.loads(my_file)

    except Exception as e:

        logger.critical("config.json invalid. Exiting.")
        logger.debug(e)
        sys.exit()

    if config.get(key):

        return config.get(key)

    else:

        logger.critical(
            "{} not found in config.json or in the environment. Exiting.".format(key)
        )
        sys.exit()


def _read_file(path):
    """ Read file if it exists, and False on error.

    Arguments:
    path {string} -- Path to file.
    """

    file = Path(path)
    if not file.is_file():

        return False

    try:

        file = open(path)
        data = file.read()
        file.close()

    except Exception as e:

        logger.critical("Exception reading file.")
        logger.critical(e)

    return data


def _write_file(path, data):
    """ Write data to file, overwriting existing file if it exists. Return False on error.

    Arguments:
    path {string} -- Path to file.
    data {string} -- Content to write.
    """

    try:

        file = open(path, mode="w")
        file.write(data)
        file.close()

    except Exception as e:

        logger.critical("Exception writing file.")
        logger.critical(e)

        return False

    return True
