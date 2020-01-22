#!.env/bin/python

import argparse
import datetime
from torrents import transmission
from time import sleep


def main(arguments):
    interval = datetime.timedelta(0, arguments.interval)
    stored_time = datetime.datetime(2000, 1, 1)

    while True:
        if stored_time + interval <= datetime.datetime.now():
            transmission.add_torrent()
            stored_time = datetime.datetime.now()
        else:
            time_remain = stored_time + interval - datetime.datetime.now()
            sleep(time_remain.total_seconds())


if __name__ == '__main__':
    description = 'Process a given RSS torrent feed and add any new torrents'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-i',
        '--interval',
        default=15,
        dest='interval',
        action='store',
        help='defines the polling interval in seconds',
        type=int
        )

    main(parser.parse_args())
