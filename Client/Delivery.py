import rsa
import time
import json
from Helper import get_credentials, get_public_key


def send(sock, message):
    credentials = get_credentials()

    with open("clients.json", 'r') as file:
        clients = json.load(file)

    # encrypt the message in every user's specific public key, so they can decrypt using their private key
    messages = {client: int.from_bytes(rsa.encrypt(message.encode(), get_public_key(clients[client])), 'big') for client in clients}

    # message data will need to carry a unique message for each user, each encrypted with their specific public keys
    message_data = {
        "purpose": "message",
        "username": credentials['username'],
        "messages": json.dumps(messages),
        "status": True,
        "timestamp": time.time()
    }

    stringified = json.dumps(message_data)

    sock.send(bytes(stringified, "utf-8"))
