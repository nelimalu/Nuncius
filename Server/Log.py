import datetime


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')


def log(message):
    print(f"[{now()}]", message)


def info(message, detail):
    log(f"[{detail.upper()}/INFO] {message}")
