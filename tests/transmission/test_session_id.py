#!.env/bin/python

from ...video_rss.transmission import session_id
from .helpers import sample_request_session_id


def test_should_call_transmission_url(mocker):
    requests = mocker.patch('requests.get')
    requests.return_value = sample_request_session_id()

    session_id.get_session_id('url', 'username', 'password')

    requests.assert_called_once_with('url', auth=('username', 'password'))


def test_should_parse_output_from_transmission_and_get_session_id(mocker):
    requests = mocker.patch('requests.get')
    requests.return_value = sample_request_session_id()

    response = session_id.get_session_id('url', 'username', 'password')
    assert response == 'xzlXm3vehtAlAJVOim481B4pb2l6yfBVYQZPq0dDqoaw8U6g'
