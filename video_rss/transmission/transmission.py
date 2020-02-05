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
        self.session_id = ''

    def add_torrent(self, magnet, retry=True):
        body = self.__build_payload(magnet)
        headers = self.__build_headers()
        response = requests.post(
            self.config.transmission_url,
            body,
            headers=headers,
            auth=self.auth)
        return self.__handle_response(response, retry, magnet)

    def __handle_response(self, response, retry, magnet):
        if response.status_code == 409 and retry:
            self.session_id = session_id.get_session_id(
                self.config.transmission_url, self.auth, self.logger)

            self.add_torrent(magnet, retry=False)
        elif response.status_code == 200:
            return self.__handle_success(response)
        else:
            self.logger.log({
                'response_body': response.text,
                'response_headers': response.headers},
                'CRITICAL')

    def __build_headers(self):
        if not self.session_id:
            self.session_id = session_id.get_session_id(
                self.config.transmission_url,
                self.auth,
                self.logger)
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

    def __handle_success(self, response):
        response_obj = json.loads(response.text)

        if response_obj.get('result') == 'success':
            new_item = response_obj['arguments'].get('torrent-added')

            return new_item
        else:
            self.logger.log({
                'response_body': response.text,
                'response_headers': response.headers},
                'ERROR')
