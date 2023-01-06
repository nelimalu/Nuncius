import curses
import Delivery
from Helper import parse_timestamp, VERSION
import time


class InputCommand:
    def __init__(self, message, messages, pad_pos):
        self.message = message
        self.messages = messages
        self.pad_pos = pad_pos

    def unpack(self):
        return self.message, self.messages, self.pad_pos


def update(win, message_data, username, online):
    win.addstr(0, 0, f'[ nuncius {VERSION} -- {username} ] [ online -- {online} ] [ time -- {parse_timestamp(time.time())} ]')

    for y, msg in enumerate(message_data.messages[message_data.pad_pos:message_data.pad_pos + win.getmaxyx()[0] - 2]):
        win.addstr(y + 1, 0, msg)

    win.addstr(win.getmaxyx()[0] - 1, 0, ">" + message_data.message)


def handle_input(win, raw_input, message, messages, pad_pos, sock):
    # --ENTER
    if raw_input == 10:
        if len(message) > 0:
            pad_pos = len(messages) - win.getmaxyx()[0] + 3 if len(messages) - win.getmaxyx()[0] + 3 > 0 else 0
            Delivery.send(sock, message)

        return InputCommand("", messages, pad_pos)

    # --BACKSPACE
    if raw_input == 8:
        if len(message) > 0:
            return InputCommand(message[:-1], messages, pad_pos)
        else:
            win.move(win.getmaxyx()[0] - 1, 2)

    # --SCROLL
    if raw_input == curses.KEY_DOWN and pad_pos < len(messages) - win.getmaxyx()[0] + 2:
        pad_pos += 1
    if raw_input == curses.KEY_UP and pad_pos > 0:
        pad_pos -= 1
    if raw_input in [546, 338, 339, curses.KEY_DOWN, curses.KEY_UP, 8]:  # resizing window
        return InputCommand(message, messages, pad_pos)

    # --TYPE
    message += chr(32 if raw_input == 0 else raw_input)
    if len(message) >= win.getmaxyx()[1] - 3:
        message = message[:win.getmaxyx()[1] - 3]

    return InputCommand(message, messages, pad_pos)
