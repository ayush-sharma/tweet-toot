import json
import sys


def _config(key):
    config_file = open('.env')
    config = config_file.read()

    if not config:
        sys.exit()

    config = json.loads(config)

    if config.get(key):
        return config.get(key)

    else:
        sys.exit()

