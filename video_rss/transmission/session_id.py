#!.env/bin/python

import requests
from lxml import html


def get_session_id(url, username, password):
    response = requests.get(url, auth=(username, password))
    response_tree = html.fromstring(response.text)
    id_value = response_tree.xpath('//code/text()')[0]
    return id_value.split(':')[1].strip()
