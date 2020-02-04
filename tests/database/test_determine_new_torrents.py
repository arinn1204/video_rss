#!.env/bin/python

import uuid

from ...video_rss.database import database
from ...video_rss import configuration
from . import database_helpers


def test_queries_based_on_torrent_id_entered(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    id = str(uuid.uuid4())

    called_id = {
        'id': id
    }
    (_, mock_cursor, _) = database_helpers.setup_mocks(mocker)
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
    (_, mock_cursor, _) = database_helpers.setup_mocks(mocker)
    db.determine_new_torrents(called_id)

    mock_cursor.execute.assert_called_once_with(f"SELECT new_ids.id FROM rss.video_rss rss RIGHT JOIN (SELECT '{id1}' AS 'id' UNION ALL SELECT '{id2}' AS 'id') new_ids ON rss.torrent_id = new_ids.id WHERE magnet IS NULL;")  # noqa: E501


def test_fetches_all_entries_from_query(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = {
        'id': str(uuid.uuid4())
    }
    (_, _, mock_execute) = database_helpers.setup_mocks(mocker)
    db.determine_new_torrents([called_id])
    mock_execute.fetchall.assert_called_once_with()


def test_returns_available_rows(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    called_id = {
        'id': str(uuid.uuid4())
    }

    (_, _, mock_execute) = database_helpers.setup_mocks(mocker)
    rows = db.determine_new_torrents([called_id])
    assert rows == [1]


def test_should_return_empty_array_if_no_ids_entered(mocker):
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    result = db.determine_new_torrents([])

    assert result == []
