import argparse
import os.path
import time
from sys import argv

import requests as r
import logging
import threading

from pip._internal.utils import urls

WORKING = list()
ALL: bool = True
TIMEOUT: int = 5


def is_error_code(c: str) -> bool:
    if c.isdigit():
        return int(c) >= 400
    else:
        return c == 'Exception'


def test_next_url(URLS: list, timeout: int = TIMEOUT):
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
        if not is_error_code(status) or ALL:
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
    sleep_time = len(urls) * .5
    w = test(urls)
    while len(urls) != 0:
        time.sleep(1)
    time.sleep(sleep_time)
    return w


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run through the list of urls and get all the working sites.')
    parser.add_argument('source',
                        metavar='SOURCE',
                        type=str,
                        help='A path to the file containing the links to sites (one link per line)',
                        action='store'
                        )
    parser.add_argument('-a', '--all', action='store_true', help='A flag to display all the sites. Default is False, '
                                                                 'displays only working sites')
    parser.add_argument('-t', '--timeout', type=int, action='store', default=5, help='A request timeout in seconds. By'
                                                                                     ' default, 5')

    args = parser.parse_args(argv[1:])
    PATH = args.source
    ALL = args.all
    TIMEOUT = args.timeout

    if not os.path.exists(PATH):
        print('File does not exist: %s' % PATH)
        exit(1)

    with open(PATH, 'r', encoding='utf-8') as f:
        urls = [u.strip() for u in f.readlines() if not u.strip().startswith('#')]

    test(urls)
