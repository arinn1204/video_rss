#!.env/bin/python

import os
import uuid
import re

from ...video_rss import configuration
from ...video_rss.database import database


def teardown_method(method):
    for key in os.environ.keys():
        if bool(re.match('^database', key, re.I)):
            os.environ.pop(key, None)


def test_constructing_proper_connection_string_for_sql_server_with_sspi(mocker):  # noqa: E501
    connect_mocker = mocker.Mock()
    mocker.patch('pyodbc.connect', new=connect_mocker)
    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)

    db.get_by_id(str(uuid.uuid4()))
    connect_mocker.assert_called_once_with('Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;Integrated Security=SSPI;')  # noqa: E501


def test_constructing_proper_connection_string_for_sql_server_without_sspi(mocker):  # noqa: E501
    connect_mocker = mocker.Mock()
    mocker.patch('pyodbc.connect', new=connect_mocker)

    os.environ['database_integrated_security'] = ''
    os.environ['database_username'] = 'userID'
    os.environ['database_password'] = 'hunter2'

    config = configuration.Configuration()
    logger = mocker.Mock()
    db = database.Database(config, logger)
    db.get_by_id(str(uuid.uuid4()))

    connect_mocker.assert_called_once_with('Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;User ID=userID;Password=hunter2;')  # noqa: E501
