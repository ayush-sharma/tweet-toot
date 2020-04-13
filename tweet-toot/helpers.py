#!/usr/bin/env python3

import datetime
import json
from pathlib import Path
import sys


def _config(key):
    """ Return configuration values from the config.json file.

    Arguments:
    key {string} -- Name of the key in the config.json file.
    """

    my_file = _read_file("config.json")
    if not my_file:
        print("--- Main config.json file not found. Exiting.")
        sys.exit()

    try:

        config = json.loads(my_file)

    except:

        print("--- config.json invalid. Exiting.")
        sys.exit()

    if config.get(key):
        return config.get(key)
    else:
        print("--- config.json invalid. Exiting.")
        sys.exit()


def _info(message):
    """ Print info messages to the console.

    Arguments:
    message {string} -- Log message.
    """
    print(f" _info > {message}")


def _error(message):
    """ Print error messages to the console.

    Arguments:
    message {string} -- Log message.
    """
    print(f" _error > {message}")


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

        _error("Exception reading file.")
        _error(e)

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

        _error("Exception writing file.")
        _error(e)

        return False

    return True
