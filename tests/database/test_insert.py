#!.env/bin/python

import uuid
import pyodbc
from datetime import datetime

from ...video_rss.database import database
from ...video_rss import configuration
from . import database_helpers


def test_inserts_new_rss_entry(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = str(uuid.uuid4())
    called_time = str(datetime.now())

    (_, mock_cursor, _) = database_helpers.setup_mocks(mocker)
    db.insert(
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


def test_should_return_rowcount(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = str(uuid.uuid4())
    called_time = str(datetime.now())

    (_) = database_helpers.setup_mocks(mocker)
    row_count = db.insert(
        called_id,
        'some file name',
        called_time,
        'magnet?:somelinkhere.')

    assert row_count == 1


def test_should_commit_if_success(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = str(uuid.uuid4())
    called_time = str(datetime.now())

    (connection, _, _) = database_helpers.setup_mocks(mocker)
    db.insert(
        called_id,
        'some file name',
        called_time,
        'magnet?:somelinkhere.')
    connection.commit.assert_called_once_with()
    connection.rollback.assert_not_called()


def test_should_rollback_on_failure(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = str(uuid.uuid4())
    called_time = str(datetime.now())

    (connection, mock_cursor, _) = database_helpers.setup_mocks(mocker)
    mock_cursor.execute.side_effect = pyodbc.DatabaseError(
        'INSERT failed in rss.video_rss')

    db.insert(
        called_id,
        'some file name',
        called_time,
        'magnet?:somelinkhere.')
    connection.rollback.assert_called_once_with()
    connection.commit.assert_not_called()
