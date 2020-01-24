#!.env/bin/python

from ...video_rss import configuration
from ...video_rss import torrents
from ...video_rss.database import database
from ...video_rss.rss import rss
from ...video_rss.transmission import transmission

from unittest import mock


@mock.patch(f"{database.__name__}.Database")
@mock.patch(f"{rss.__name__}.Rss")
@mock.patch(f"{transmission.__name__}.Transmission")
def test_should_check_new_torrents_with_db(magic_transmission, magic_rss, magic_db):  # noqa: E501
    mock_transmission = mock.Mock()
    mock_rss = mock.Mock()
    mock_db = mock.Mock()

    magic_transmission.return_value = mock_transmission
    magic_db.return_value = mock_db
    magic_rss.return_value = mock_rss

    expected = {
        'hashString': '011b282e690e127b90d2f33aeb29686dd739d951',
        'id': 15,
        'name': 'TRON+-+Legacy+(2010)+(1080p+BluRay+x265+HEVC+10bit+AAC+7.1+Tigole)+[QxR]'  # noqa: E501
    }
    mock_rss.get_videos.return_value = [{
        'title': 'title',
        'magnet': 'magnet:?',
        'id': 'some_id_here'
    }]

    mock_db.determine_new_torrents.return_value = ['some_id_here']
    mock_db.insert.return_value = 1

    mock_transmission.add_torrent.return_value = expected

    config = configuration.Configuration()

    print(mock_rss.get_videos())
    print(mock_db.determine_new_torrents())
    print(mock_db.insert())
    print(mock_transmission.add_torrent())

    added_torrents = torrents.add_torrent(config)
    assert added_torrents == [expected]
