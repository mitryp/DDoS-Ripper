import time
from sys import argv

import requests as r
import logging
import threading

WORKING = list()


def is_error_code(c) -> bool:
    if type(c) == str:
        return c == 'Exception'
    elif type(c) == int:
        return c >= 400
    return True


def test_next_url(URLS: list, timeout: int = 5):
    if not URLS:
        return None

    url = URLS.pop().strip().replace('\n', '')
    if not url.startswith('http'):
        url = 'http://' + url

    status: str
    try:
        req = r.get(url, timeout=timeout)
        status = str(req.status_code)
    except r.exceptions.RequestException:
        status = 'Exception'

    if __name__ == '__main__':
        logging.info(f'{url} {status=}')

    if not is_error_code(status):
        WORKING.append(url)


def test(urls: list) -> list:
    WORKING.clear()
    fmt = "%(message)s"
    logging.basicConfig(format=fmt, level=logging.INFO)
    while len(urls) != 0:
        for _ in range(10):
            threading.Thread(target=test_next_url, args=(urls, 5)).start()
        time.sleep(.01)

    return WORKING


def get_working_sites(urls: list) -> list:
    print("Getting new list of working sites")
    sleep_time = len(urls)*.5
    w = test(urls)
    while len(urls) != 0:
        time.sleep(1)
    time.sleep(sleep_time)
    print(w)
    return w


if __name__ == '__main__':
    URLS_PATH = argv[1]
    with open(URLS_PATH, 'r', encoding='utf-8') as f:
        urls = f.readlines()

    test(urls)

