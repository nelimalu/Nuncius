import json
import rsa
import datetime
from pytz import timezone

VERSION = 'v1.2'
RECV_BYTES = 8192


def parse_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern')).strftime('%H:%M:%S')


def get_credentials():
    with open("client_credentials.json", 'r') as file:
        return json.load(file)


def get_public_key(public_key):
    return rsa.PublicKey(
        public_key['n'],
        public_key['e']
    )


def get_private_key(private_key):
    return rsa.PrivateKey(
        private_key['n'],
        private_key['e'],
        private_key['d'],
        private_key['p'],
        private_key['q']
    )
