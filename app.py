# Let's import Marvel stuff
import argparse
import requests
import time
import hashlib
import json

# Let's get Singer stuff
import singer
import urllib.request
from datetime import datetime, timezone

# let's setup to get the config file for the keys
REQUIRED_CONFIG_KEYS = ['private_key', 'public_key']
CONFIG = {}


# let's hold our info in f
def load_json(path):
    with open(path) as f:
        return json.load(f)


# add to the command line so we can talk to the config file
def parse_args(required_config_keys):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    args = parser.parse_args()

    config = load_json(args.config)
    check_config(config, required_config_keys)

    return config


# make sure we have our keys
def check_config(config, required_keys):
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise Exception("Config is missing required keys: {}".format(missing_keys))

    # let's get marvel going


def get_characters():
    marvel_limit = 100
    offset = 0

    # Format the time
    t = time.strftime("%Y%d%m%H%M%S")
    m = hashlib.md5()

    m.update("{}{}{}".format(t, CONFIG['private_key'], CONFIG['public_key']).encode("utf-8"))

    hash = m.hexdigest()

    # Now let's get Singer going
    schema = {'type': 'object',
              'properties':
                  {
                      'id': {'type': 'integer'},
                      'name': {'type': 'string'},
                      'modified': {'type': 'string', 'format': 'date-time'}
                  }}

    singer.write_schema('characters', schema, 'id')

    # call the api and get records until there aren't anymore
    while True:
        response = requests.get(
            'https://gateway.marvel.com:443/v1/public/characters?orderBy=modified&apikey={}&ts={}&hash={}&limit={}&offset={}'.format(
                CONFIG['public_key'], t, hash, marvel_limit, offset))

        body = response.json()['data']

        singer.write_records('characters', body['results'])

        offset = offset + marvel_limit

        if body['count'] < marvel_limit:
            break


# run this puppy
def main():
    CONFIG.update(parse_args(REQUIRED_CONFIG_KEYS))
    get_characters()


# do main first
if __name__ == '__main__':
    main()