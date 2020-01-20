#!.env/bin/python

import requests
from lxml import html


def get_session_id(url, username, password, logger=None):
    response = requests.get(url, auth=(username, password))

    if logger is not None:
        logger.log(response.text, 'DEBUG')

    response_tree = html.fromstring(response.text)
    id_value = response_tree.xpath('//code/text()')[0]
    return id_value.split(':')[1].strip()
