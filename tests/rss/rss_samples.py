#!.env/bin/python
# flake8: noqa

import json
import pathlib
import os


def get_showrss_sample():
    with open(_get_path('showrss.json'), 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
    return data

def get_showrss_sample_with_one_entry():
    with open(_get_path('showrss_one_item.json'), 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
    return data

def get_showrss_sample_with_two_entries():
    with open(_get_path('showrss_two_items.json'), 'r') as file:
        json_data = file.read()
        data = json.loads(json_data)
    return data

def _get_path(path):
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path + os.path.sep + path