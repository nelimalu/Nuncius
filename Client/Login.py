from pwinput import pwinput
import time
import json
from hashlib import sha512
from os import system as sys
import rsa


def confirm_identity(sock, credentials):
    send_data = {
        "purpose": "login",
        "username": credentials['username'],
        "password": credentials['password'],
        "status": True,
        "public_key": credentials['public_key'],
        "timestamp": time.time()
    }

    sock.send(bytes(json.dumps(send_data), "utf-8"))

    recieved = json.loads(sock.recv(8192).decode())
    if recieved["purpose"] == "login" and not recieved["status"]:
        print("denied")
        sock.close()
        quit()

    elif recieved["purpose"] == "login" and recieved["status"]:
        with open("clients.json", 'w') as file:
            json.dump(recieved['public_keys'], file, indent=4)

    print("granted")


def verify_credentials(sock):
    sys('cls')
    print("[ nuncius -- login ]")
    username = input("> Username: ")
    password = pwinput("> Password: ")
    print("> Login entry:", end=" ")

    public_key, private_key = rsa.newkeys(1024)

    credentials = {
        "username": username,
        "password": sha512(password.encode()).hexdigest(),
        "status": True,
        "public_key": {
            "e": public_key.e,
            "n": public_key.n
        },
        "private_key": {
            "e": private_key.e,
            "n": private_key.n,
            "d": private_key.d,
            "p": private_key.p,
            "q": private_key.q,
        }
    }

    with open("client_credentials.json", "w") as file:
        json.dump(credentials, file, indent=4)

    with open("clients.json", 'w') as file:
        json.dump({}, file)

    return confirm_identity(sock, credentials)
