#!.env/bin/python
# flake8: noqa

from ...video_rss.rss import rss as sut
from ...video_rss import configuration

from .rss_samples import get_showrss_sample_with_one_entry


def test_should_parse_feed_from_config(mocker):
    feedparser = mocker.patch('feedparser.parse')
    logger = mocker.Mock()
    config = configuration.Configuration()
    config.rss_feed_address = 'showrss.info/test_should_parse_feed_from_config'
    rss = sut.Rss(config, logger)
    _ = [i for i in rss.get_videos()]

    feedparser.assert_called_once_with('showrss.info/test_should_parse_feed_from_config')


def test_should_retrieve_all_rss_objects(mocker):
    feedparser = mocker.patch('feedparser.parse')
    feedparser.return_value = get_showrss_sample_with_one_entry()
    logger = mocker.Mock()
    config = configuration.Configuration()
    config.rss_feed_address = 'showrss.info/user'
    rss = sut.Rss(config, logger)

    data = [i for i in rss.get_videos()]
    assert len(data) == 1

    assert data[0] == {
        'title': 'Vikings S06E07 720p WEB H264 GHOSTS',
        'magnet': 'magnet:?xt=urn:btih:743E0F4656DFD378420C6C8B9127121B1D656E3A&dn=Vikings+S06E07+720p+WEB+H264+GHOSTS&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce',
        'id': 'cc4a6cca13da8d2483e88c2e640027857aef64a7'}
