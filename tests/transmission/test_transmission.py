#!.env/bin/python

from ...video_rss.transmission.transmission import Transmission
from ...video_rss.transmission import session_id
from ...video_rss.configuration import Configuration
from . import helpers
import uuid
from unittest import mock
from unittest.mock import call
from json import dumps


def test_should_add_supplied_torrent(mocker):
    with mock.patch(f"{session_id.__name__}.get_session_id") as mocked_session:
        fake_session_id = str(uuid.uuid4())
        mocked_session.return_value = fake_session_id
        logger = mocker.Mock()

        transmission = Transmission(build_config(), logger)

        with mock.patch('requests.post') as mocked_request:
            fake_request = helpers.sample_request_session_id()
            fake_request.text = '{"arguments":{"torrent-added":{"hashString":"011b282e690e127b90d2f33aeb29686dd739d951","id":15,"name":"TRON+-+Legacy+(2010)+(1080p+BluRay+x265+HEVC+10bit+AAC+7.1+Tigole)+[QxR]"}},"result":"success"}\n'  # noqa: E501

            mocked_request.return_value = fake_request
            transmission.add_torrent('magnet://')

            mocked_request.assert_called_once_with(
                'url',
                dumps({'method': 'torrent-add',
                       'arguments': {'filename': 'magnet://'}}),
                headers={
                    'X-Transmission-Session-Id': fake_session_id
                },
                auth=('username', 'password'))


def test_should_get_new_session_id_if_409_returned(mocker):
    with mock.patch(f"{session_id.__name__}.get_session_id") as mocked_session:
        fake_session_id = str(uuid.uuid4())
        mocked_session.return_value = fake_session_id
        logger = mocker.Mock()
        get_session = call('url', ('username', 'password'), logger)

        transmission = Transmission(build_config(), logger)

        with mock.patch('requests.post') as mocked_request:
            fake_request = helpers.sample_request_session_id()
            fake_request.status_code = 409

            mocked_request.return_value = fake_request

            transmission.add_torrent('magnet://')

            mocked_session.assert_has_calls([
                get_session, get_session
            ])


def test_should_return_argument_object_on_success(mocker):
    with mock.patch(f"{session_id.__name__}.get_session_id") as mocked_session:
        fake_session_id = str(uuid.uuid4())
        mocked_session.return_value = fake_session_id
        logger = mocker.Mock()

        transmission = Transmission(build_config(), logger)

        with mock.patch('requests.post') as mocked_request:
            fake_request = helpers.sample_request_session_id()
            fake_request.status_code = 200
            fake_request.text = '{"arguments":{"torrent-added":{"hashString":"011b282e690e127b90d2f33aeb29686dd739d951","id":15,"name":"TRON+-+Legacy+(2010)+(1080p+BluRay+x265+HEVC+10bit+AAC+7.1+Tigole)+[QxR]"}},"result":"success"}\n'  # noqa: E501

            mocked_request.return_value = fake_request

            response = transmission.add_torrent('magnet://')

            assert response == {
                'hashString': '011b282e690e127b90d2f33aeb29686dd739d951',
                'id': 15,
                'name': 'TRON+-+Legacy+(2010)+(1080p+BluRay+x265+HEVC+10bit+AAC+7.1+Tigole)+[QxR]'  # noqa: E501
            }


def build_config():
    config = Configuration()
    config.transmission_url = 'url'
    config.transmission_username = 'username'
    config.transmission_password = 'password'
    return config
