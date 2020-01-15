#!.env/bin/python

from ...video_rss.rss import rss as sut
from ...video_rss import configuration


def test_should_parse_feed_from_config(mocker):
    feedparser = mocker.patch('feedparser.parse')
    logger = mocker.Mock()
    config = configuration.Configuration()
    config.rss_feed_address = 'showrss.info/user'
    rss = sut.Rss(config, logger)
    rss.get_videos()

    feedparser.assert_called_once_with('showrss.info/user')
