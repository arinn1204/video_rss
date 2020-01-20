#!.env/bin/python

from ...video_rss.transmission.transmission import Transmission
from ...video_rss.transmission import session_id
from ...video_rss.configuration import Configuration
from . import helpers
import uuid
from unittest import mock
from json import dumps


def test_should_add_supplied_torrent(mocker):
    with mock.patch(f"{session_id.__name__}.get_session_id") as mocked_session:
        fake_session_id = str(uuid.uuid4())
        mocked_session.return_value = fake_session_id
        logger = mocker.Mock()

        transmission = Transmission(build_config(), logger)

        with mock.patch('requests.post') as mocked_request:
            mocked_request.return_value = helpers.sample_request_session_id()
            transmission.add_torrent('magnet://')

            mocked_request.assert_called_once_with(
                'url',
                dumps({'method': 'torrent-add',
                       'arguments': {'filename': 'magnet://'}}),
                headers={
                    'X-Transmission-Session-Id': fake_session_id
                },
                auth=('username', 'password'))


def build_config():
    config = Configuration()
    config.transmission_url = 'url'
    config.transmission_username = 'username'
    config.transmission_password = 'password'
    return config
