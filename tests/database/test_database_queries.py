#!.env/bin/python

import os
import re
import uuid
import pyodbc
from datetime import datetime

from ...video_rss.database import database
from ...video_rss import configuration


class TestDatabaseQueries:
    def setup_method(self, method):
        self.config = configuration.Configuration()
        self.database = database.Database(self.config)

    def teardown_method(self, method):
        for key in os.environ.keys():
            if bool(re.match('^database', key, re.I)):
                self.__delete_if_exist(key)

    def test_queries_based_on_torrent_id_entered(self, mocker):
        called_id = str(uuid.uuid4())

        (_, mock_cursor, _) = self.__setup_mocks(mocker)
        self.database.get_by_id(called_id)

        mock_cursor.execute.assert_called_once_with("""
        SELECT 1
        FROM rss.video_rss
        WHERE torrent_id = ?;""", called_id)

    def test_fetches_all_entries_from_query(self, mocker):
        called_id = str(uuid.uuid4())

        (_, _, mock_execute) = self.__setup_mocks(mocker)
        self.database.get_by_id(called_id)
        mock_execute.fetchall.assert_called_once_with()

    def test_returns_available_rows(self, mocker):
        called_id = str(uuid.uuid4())

        (_, _, mock_execute) = self.__setup_mocks(mocker)
        rows = self.database.get_by_id(called_id)
        assert rows == [(1,)]

    def test_inserts_new_rss_entry(self, mocker):
        called_id = str(uuid.uuid4())
        called_time = str(datetime.now())

        (_, mock_cursor, _) = self.__setup_mocks(mocker)
        self.database.insert(
            called_id,
            'some file name',
            called_time,
            'magnet?:somelinkhere.')

        query = """
        INSERT INTO rss.video_rss(torrent_id,torrent_name,time_added,magnet)
        VALUES(?, ?, ?, ?)"""

        mock_cursor.execute.assert_called_once_with(
            query,
            called_id,
            'some file name',
            called_time,
            'magnet?:somelinkhere.')

    def test_should_return_rowcount(self, mocker):
        called_id = str(uuid.uuid4())
        called_time = str(datetime.now())

        (_) = self.__setup_mocks(mocker)
        row_count = self.database.insert(
            called_id,
            'some file name',
            called_time,
            'magnet?:somelinkhere.')

        assert row_count == 1

    def test_should_commit_if_success(self, mocker):
        called_id = str(uuid.uuid4())
        called_time = str(datetime.now())

        (connection, _, _) = self.__setup_mocks(mocker)
        self.database.insert(
            called_id,
            'some file name',
            called_time,
            'magnet?:somelinkhere.')
        connection.commit.assert_called_once_with()
        connection.rollback.assert_not_called()

    def test_should_rollback_on_failure(self, mocker):
        called_id = str(uuid.uuid4())
        called_time = str(datetime.now())

        (connection, mock_cursor, _) = self.__setup_mocks(mocker)
        mock_cursor.execute.side_effect = pyodbc.DatabaseError(
            'INSERT failed in rss.video_rss')

        self.database.insert(
            called_id,
            'some file name',
            called_time,
            'magnet?:somelinkhere.')
        connection.rollback.assert_called_once_with()
        connection.commit.assert_not_called()

    def __setup_mocks(self, mocker):
        mock_pyodbc_connection = mocker.Mock()
        mock_connection = mocker.Mock()
        mock_cursor = mocker.Mock()
        mock_execute = mocker.Mock()

        mock_pyodbc_connection = mocker.patch('pyodbc.connect')
        mock_pyodbc_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = mock_execute
        mock_execute.fetchall.return_value = [(1,)]
        mock_execute.rowcount.return_value = 1

        return (mock_connection, mock_cursor, mock_execute)
