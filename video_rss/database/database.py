#!.env/bin/python

import pyodbc
from .connection_string_helper import build_connection_string


class Database:
    def __init__(self, config):
        self.config = config

    def get_by_id(self, torrent_id):
        query = """
        SELECT 1
        FROM rss.video_rss
        WHERE torrent_id = ?;"""

        connection = self.__get_connection()
        cursor = connection.cursor()
        rows = cursor.execute(query, torrent_id)
        data = rows.fetchall()

        connection.close()

        return data

    def insert(self, torrent_id, torrent_file, added_time, magnet_link):
        query = """
        INSERT INTO rss.video_rss(torrent_id,torrent_name,time_added,magnet)
        VALUES(?, ?, ?, ?)"""
        entries_effected = 0

        connection = self.__get_connection()
        cursor = connection.cursor()

        try:
            rows = cursor.execute(
                query,
                torrent_id,
                torrent_file,
                added_time,
                magnet_link)
            entries_effected = rows.rowcount()
        except pyodbc.DatabaseError:
            connection.rollback()
        else:
            connection.commit()
        finally:
            connection.close()

        return entries_effected

    def __get_connection(self):
        connection_string = build_connection_string(self.config)
        connection = pyodbc.connect(connection_string)
        return connection
