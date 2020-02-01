#!.env/bin/python

import pyodbc
from .connection_string_helper import build_connection_string


class Database:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def determine_new_torrents(self, torrents):
        ids = [torrent['id'] for torrent in torrents]
        unions = ''
        if len(ids) > 1:
            unions = ' '.join([f"UNION ALL SELECT '{id}' AS 'id'" for id in ids[1:]])  # noqa: E501
        sub_query = f"SELECT '{ids[0]}' AS 'id' {unions}"

        query = f"SELECT new_ids.id FROM rss.video_rss rss RIGHT JOIN ({sub_query}) new_ids ON rss.torrent_id = new_ids.id WHERE magnet IS NULL;"  # noqa: E501

        # query = "EXEC rss.usd_new_ids ?;"
        self.logger.log(query, 'DEBUG')

        connection = self.__get_connection()
        cursor = connection.cursor()
        rows = cursor.execute(query).fetchall()
        cursor.close()
        connection.close()

        data = [row[0] for row in rows]

        if len(data) > 0:
            self.logger.log(f"new ids: {data}", 'INFO')

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
            entries_effected = rows.rowcount
        except pyodbc.DatabaseError as e:
            connection.rollback()
            self.logger.log(e, 'ERROR')
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()

        self.logger.log(f"Rows effected: {entries_effected}", 'INFO')
        return entries_effected

    def __get_connection(self):
        connection_string = build_connection_string(self.config)
        connection = pyodbc.connect(connection_string)
        return connection
