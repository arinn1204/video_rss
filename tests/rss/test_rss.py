#!.env/bin/python

from feedparser import parse as fp_parse
from ...video_rss.rss import rss as sut
from ...video_rss import configuration

from . import rss_samples


def test_should_parse_feed_from_config(mocker):
    return_data = fp_parse(rss_samples.get_sample_with_two_items())
    feedparser = mocker.patch('feedparser.parse')
    feedparser.return_value = return_data
    logger = mocker.Mock()
    config = configuration.Configuration()

    config.rss_feed_address = 'showrss.info/user'
    rss = sut.Rss(config, logger)
    rss.get_videos()

    feedparser.assert_called_once_with('showrss.info/user')
