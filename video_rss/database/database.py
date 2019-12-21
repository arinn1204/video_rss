#!.env/bin/python

import pyodbc

from .connection_string_helper import build_connection_string


class Database:
    def __init__(self, config):
        self.config = config

    def get_by_id(self, torrent_id):
        connection_string = build_connection_string(self.config)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = self.__query_by_id()
        rows = cursor.execute(query, torrent_id)

        return rows.fetchall()

    def __query_by_id(self):
        return """
        SELECT 1
        FROM rss.video_rss
        WHERE torrent_id = ?;"""
