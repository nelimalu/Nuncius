import socket
import json
from threading import *
import time
import Log
import copy

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.50.242'
port = 5431
serversocket.bind((host, port))

with open("users.json", "r") as file:
    users = json.loads(file.read())

clients = []


def loop_sockets():
    return [client.sock for client in clients]


def get_public_keys():
    return {client.credentials['username']: client.credentials['public_key'] for client in clients}


def remove_client(sock):
    global clients

    for client in clients:
        if client.sock == sock:
            clients.remove(client)
            break


def find_client(username):
    for client in clients:
        if client.credentials['username'] == username:
            return client


class Client(Thread):
    def __init__(self, _socket, _address):
        Thread.__init__(self)
        self.sock = _socket
        self.addr = _address
        self.credentials = None
        self.start()

    def run(self):
        while True:
            try:
                recv = self.sock.recv(8192).decode()
                if len(recv) == 0:
                    if self.credentials is not None:
                        self.handle_logout()
                    if self in clients:
                        clients.remove(self)
                    break

                recieved = json.loads(recv)

                # <MESSAGE HANDLING>

                if recieved["purpose"] == "message":
                    messages = json.loads(recieved['messages'])
                    Log.info(f"Recieved message from {self.credentials['username']}", "MESSAGE")

                    for username in messages.keys():
                        send_data = {
                            "purpose": "message",
                            "status": True,
                            "timestamp": time.time(),
                            "username": self.credentials['username'],
                            "message": messages[username]
                        }

                        client = find_client(username)
                        client.sock.send(bytes(json.dumps(send_data), 'utf-8'))

                elif recieved["purpose"] == "login":
                    self.handle_login(recieved)

                # </MESSAGE HANDLING>

            except ConnectionResetError:
                self.handle_logout()
                break

    def handle_logout(self):
        Log.info(f"Client {self.credentials['username']} disconnected", "LOGOUT")
        send_data = {
            "purpose": "logout",
            "status": True,
            "timestamp": time.time(),
            "username": self.credentials['username']
        }

        if self in clients:
            clients.remove(self)

        for sock in loop_sockets():
            sock.send(bytes(json.dumps(send_data), 'utf-8'))

    def failed_login(self, package):
        Log.info(f"Client {package['username']} not found in users list.", "LOGIN")

        send_data = {
            "purpose": "login",
            "status": False,
            "timestamp": time.time()
        }

        self.sock.send(bytes(json.dumps(send_data), 'utf-8'))
        clients.remove(self)

    def handle_login(self, package):
        if package['username'] not in users.keys():
            return self.failed_login(package)

        self.credentials = copy.deepcopy(package)
        del self.credentials['password']
        Log.info(f"Client {package['username']} connected", "LOGIN")

        send_data = {
            "purpose": "login",
            "status": package['username'] in users.keys() and package['password'] == users[package['username']],
            "timestamp": time.time()
        }
        # send everyone's public keys only if user logs in properly
        send_data['public_keys'] = get_public_keys() if send_data['status'] else None

        self.sock.send(bytes(json.dumps(send_data), 'utf-8'))

        if send_data['status']:
            for sock in loop_sockets():
                try:
                    sock.send(bytes(json.dumps(self.credentials), 'utf-8'))
                except ConnectionAbortedError:
                    remove_client(sock)


serversocket.listen(5)
Log.info("Server started and listening", "STARTUP")
try:
    while True:
        clientsocket, address = serversocket.accept()
        clients.append(Client(clientsocket, address))
finally:
    serversocket.close()
