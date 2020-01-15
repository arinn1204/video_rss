#!.env/bin/python

import pyodbc
from .connection_string_helper import build_connection_string


class Database:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def get_by_id(self, torrent_id):
        query = """
        SELECT torrent_id, torrent_name, time_added
        FROM rss.video_rss
        WHERE torrent_id = ?;"""

        self.logger.log(query, 'DEBUG')

        connection = self.__get_connection()
        cursor = connection.cursor()
        rows = cursor.execute(query, torrent_id)
        data = rows.fetchall()

        cursor.close()
        connection.close()

        self.logger.log(data, 'DEBUG')

        return data

    def insert(self, torrent_id, torrent_file, added_time, magnet_link):
        query = """
        INSERT INTO rss.video_rss(torrent_id,torrent_name,time_added,magnet)
        VALUES(?, ?, ?, ?)"""
        entries_effected = 0

        self.logger.log(query, 'DEBUG')

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
        except pyodbc.DatabaseError as e:
            connection.rollback()
            self.logger.log(e, 'ERROR')
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()

        self.logger.log(f"Rows effected: {entries_effected}", 'DEBUG')
        return entries_effected

    def __get_connection(self):
        connection_string = build_connection_string(self.config)
        connection = pyodbc.connect(connection_string)
        return connection
