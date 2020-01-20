#!.env/bin/python

from ...video_rss.transmission import session_id


def test_should_call_transmission_url(mocker):
    requests = mocker.patch('requests.get')

    session_id.get_session_id('url', 'username', 'password')

    requests.assert_called_once_with('url', auth=('username', 'password'))
