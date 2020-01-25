#!.env/bin/python

import argparse
import datetime
from time import sleep
from video_rss.configuration import Configuration
from video_rss import torrents


def main(arguments):
    interval = datetime.timedelta(0, arguments.interval)
    stored_time = datetime.datetime(2000, 1, 1)
    config = Configuration()

    while True:
        if stored_time + interval <= datetime.datetime.now():
            torrents.add_torrent(config, arguments.dry_run)
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
        type=int)

    parser.add_argument(
        '-d',
        '--dry-run',
        default=False,
        dest='dry_run',
        action='store_true',
        help='runs application in dry state and performs no writes')

    main(parser.parse_args())
