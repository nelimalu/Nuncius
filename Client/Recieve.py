import json
import rsa
from Helper import get_credentials, get_private_key, parse_timestamp
import math


def parse(message_data):
    purpose = message_data['purpose']
    status = message_data['status']

    if not status:
        return

    if purpose == "login":
        return handle_login(message_data)

    if purpose == "message":
        return handle_message(message_data)

    if purpose == "logout":
        return handle_logout(message_data)


def handle_message(message_data):
    credentials = get_credentials()
    private_key = get_private_key(credentials['private_key'])

    bytes_required = max(1, math.ceil(message_data['message'].bit_length() / 8))
    message_bytes = message_data['message'].to_bytes(bytes_required, 'big')
    message = rsa.decrypt(message_bytes, private_key).decode()

    return f"[{parse_timestamp(message_data['timestamp'])}] {message_data['username']}: {message}"


def handle_login(message_data):
    with open("clients.json", 'r') as file:
        clients = json.load(file)

    clients[message_data['username']] = message_data['public_key']

    with open("clients.json", 'w') as file:
        json.dump(clients, file, indent=4)

    return f'[{parse_timestamp(message_data["timestamp"])}] [LOGIN] User "{message_data["username"]}" connected.'


def handle_logout(message_data):
    with open("clients.json", 'r') as file:
        clients = json.load(file)

    del clients[message_data['username']]

    with open("clients.json", 'w') as file:
        json.dump(clients, file, indent=4)

    return f'[{parse_timestamp(message_data["timestamp"])}] [LOGOUT] User "{message_data["username"]}" disconnected.'

