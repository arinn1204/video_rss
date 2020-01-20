#!.env/bin/python

import requests


def get_session_id(url, username, password):
    response = requests.get(url, auth=(username, password))
    return response
