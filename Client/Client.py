import socket
from curses import wrapper
import GUI
import Login
from threading import Thread
import Recieve
import json
from Helper import get_credentials, RECV_BYTES

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('99.241.147.138', 5431))
s.settimeout(5)

messages = []
run = True


def listener():
    global messages, run

    while run:
        try:
            recieved = s.recv(RECV_BYTES).decode()
            message = Recieve.parse(json.loads(recieved))

            if message is not None:
                messages.append(message)
        except ConnectionResetError:
            run = False
        except socket.timeout:
            pass

    s.close()


def main(win):
    global messages, run
    win.nodelay(True)

    message = ""
    pad_pos = 0

    username = get_credentials()['username']

    while run:
        win.erase()

        try:
            with open('clients.json', 'r') as file:
                online = len(json.load(file))
        except json.decoder.JSONDecodeError:
            online = "?"

        GUI.update(win, GUI.InputCommand(message, messages, pad_pos), username, online)

        raw_input = win.getch()
        if raw_input != -1:
            message, messages, pad_pos = GUI.handle_input(win, raw_input, message, messages, pad_pos, s).unpack()
            if raw_input == 27 or message == ".quit":
                run = False

        win.refresh()


if __name__ == "__main__":
    Login.verify_credentials(s)

    server_listener = Thread(target=listener, args=[])
    server_listener.start()

    wrapper(main)

    print("> Quitting nuncius...")

    server_listener.join()
