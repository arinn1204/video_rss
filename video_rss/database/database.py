#!env/bin/python

import pyodbc

from .connection_string_helper import build_connection_string

class Database:
    def __init__(self, config):
        self.config = config

    def get_by_id(self, torrent_id):
        connection = self.__get_connection()

    def __get_connection(self):
        connection_string = build_connection_string(self.config)

        return pyodbc.connect(connection_string)
