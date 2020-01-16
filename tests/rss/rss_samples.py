# flake8: noqa

import json


def get_showrss_sample():
    with open('showrss.json', 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
    return data