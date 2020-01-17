#!.env/bin/python

import feedparser


class Rss:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def get_videos(self):
        rss_data = feedparser.parse(self.config.rss_feed_address)

        entries = rss_data['entries']
        for entry in entries:
            yield {
                'title': entry['title'],
                'magnet': entry['link'],
                'id': entry['id']
            }
