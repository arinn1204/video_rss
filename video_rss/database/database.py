#!.env/bin/python

import pyodbc

from .connection_string_helper import build_connection_string


class Database:
    def __init__(self, config):
        self.config = config

    def get_by_id(self, torrent_id):
        connection_string = build_connection_string(self.config)
        connection = pyodbc.connect(connection_string)
