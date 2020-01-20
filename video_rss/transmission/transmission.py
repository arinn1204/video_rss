#!.env/bin/python

from . import session_id
import requests
import json


class Transmission:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.auth = (config.transmission_username,
                     config.transmission_password)
        self.session_id = session_id.get_session_id(
            config.transmission_url, self.auth, logger)

    def add_torrent(self, magnet, retry=True):
        body = self.__build_payload(magnet)
        headers = self.__build_headers()
        response = requests.post(
            self.config.transmission_url,
            body,
            headers=headers,
            auth=self.auth)

        if response.status_code == 409 and retry:
            self.session_id = session_id.get_session_id(
                self.config.transmission_url, self.auth, self.logger)
            self.add_torrent(magnet, retry=False)

    def __build_headers(self):
        return {
            'X-Transmission-Session-Id': self.session_id
        }

    def __build_payload(self, magnet):
        return json.dumps({
            'method': 'torrent-add',
            'arguments': {
                'filename': magnet
            }
        })
