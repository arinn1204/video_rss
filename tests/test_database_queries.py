#!.env/bin/python

import os
import re
import uuid
from ..video_rss.database import database
from ..video_rss import configuration


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

        (mock_cursor, mock_execute) = self.__setup_mocks(mocker)
        self.database.get_by_id(called_id)

        mock_cursor.execute.assert_called_once_with("""
        SELECT 1
        FROM rss.video_rss
        WHERE torrent_id = ?;""", called_id)

    def test_fetches_all_entries_from_query(self, mocker):
        called_id = str(uuid.uuid4())

        (mock_cursor, mock_execute) = self.__setup_mocks(mocker)
        self.database.get_by_id(called_id)
        mock_execute.fetchall.assert_called_once_with()

    def test_returns_available_rows(self, mocker):
        called_id = str(uuid.uuid4())

        (mock_cursor, mock_execute) = self.__setup_mocks(mocker)
        rows = self.database.get_by_id(called_id)
        assert rows == [(1,)]

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

        return (mock_cursor, mock_execute)
