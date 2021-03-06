#!.env/bin/python

from .database import database
from .logging import logger
from .rss import rss
from .transmission import transmission

from datetime import datetime
import traceback


def add_torrent(config, dry_run=False):
    video_logger = logger.Logger(config)
    try:
        video_logger.log(f"Dry run state: {dry_run}", 'DEBUG')
        rss_feed = rss.Rss(config, video_logger)

        torrents = transmission.Transmission(config, video_logger)
        db = database.Database(config, video_logger)

        available_files = [i for i in rss_feed.get_videos()]
        new_ids = db.determine_new_torrents(available_files)

        new_entries = []
        for new_file in available_files:
            if new_file['id'] in new_ids and not dry_run:
                new_torrent = torrents.add_torrent(new_file['magnet'])
                new_entries.append(new_torrent)
                db.insert(
                    new_file['id'],
                    new_file['title'],
                    datetime.now(),
                    new_file['magnet'])

        if len(new_entries) > 0:
            video_logger.log(f"New Entries: {new_entries}", 'INFO')

        return new_entries
    except Exception as e:
        formatted_lines = traceback.format_exc().splitlines()
        video_logger.log(
            f"args: {e.args}, stacktrace: {formatted_lines}",
            'ERROR')
