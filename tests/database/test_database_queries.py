#!.env/bin/python

import uuid
import pyodbc
from datetime import datetime

from ...video_rss.database import database
from ...video_rss import configuration


def test_queries_based_on_torrent_id_entered(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    id = str(uuid.uuid4())

    called_id = {
        'id': id
    }
    (_, mock_cursor, _) = __setup_mocks(mocker)
    db.determine_new_torrents([called_id])

    mock_cursor.execute.assert_called_once_with(f"SELECT new_ids.id FROM rss.video_rss rss RIGHT JOIN (SELECT '{id}' AS 'id' ) new_ids ON rss.torrent_id = new_ids.id WHERE magnet IS NULL;")  # noqa: E501


def test_query_unions_all_entered_ids_together(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())

    called_id = [{
        'id': id1
    }, {
        'id': id2
    }]
    (_, mock_cursor, _) = __setup_mocks(mocker)
    db.determine_new_torrents(called_id)

    mock_cursor.execute.assert_called_once_with(f"SELECT new_ids.id FROM rss.video_rss rss RIGHT JOIN (SELECT '{id1}' AS 'id' UNION ALL SELECT '{id2}' AS 'id') new_ids ON rss.torrent_id = new_ids.id WHERE magnet IS NULL;")  # noqa: E501


def test_fetches_all_entries_from_query(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = {
        'id': str(uuid.uuid4())
    }
    (_, _, mock_execute) = __setup_mocks(mocker)
    db.determine_new_torrents([called_id])
    mock_execute.fetchall.assert_called_once_with()


def test_returns_available_rows(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = {
        'id': str(uuid.uuid4())
    }

    (_, _, mock_execute) = __setup_mocks(mocker)
    rows = db.determine_new_torrents([called_id])
    assert rows == [1]


def test_inserts_new_rss_entry(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = str(uuid.uuid4())
    called_time = str(datetime.now())

    (_, mock_cursor, _) = __setup_mocks(mocker)
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

    (_) = __setup_mocks(mocker)
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

    (connection, _, _) = __setup_mocks(mocker)
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

    (connection, mock_cursor, _) = __setup_mocks(mocker)
    mock_cursor.execute.side_effect = pyodbc.DatabaseError(
        'INSERT failed in rss.video_rss')

    db.insert(
        called_id,
        'some file name',
        called_time,
        'magnet?:somelinkhere.')
    connection.rollback.assert_called_once_with()
    connection.commit.assert_not_called()


def test_should_return_empty_array_if_no_ids_entered(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    result = db.determine_new_torrents([])

    assert result == []


def __setup_mocks(mocker):
    mocker.patch('sys.platform').return_value = 'Windows'
    mock_pyodbc_connection = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_execute = mocker.Mock()

    mock_pyodbc_connection = mocker.patch('pyodbc.connect')
    mock_pyodbc_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = mock_execute
    mock_execute.fetchall.return_value = [(1,)]
    mock_execute.rowcount = 1

    return (mock_connection, mock_cursor, mock_execute)
