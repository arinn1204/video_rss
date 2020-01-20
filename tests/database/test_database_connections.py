#!.env/bin/python

import uuid

from ...video_rss import configuration
from ...video_rss.database import connection_string_helper


def test_constructing_proper_connection_string_for_sql_server_with_sspi(mocker):  # noqa: E501
    config = configuration.Configuration()
    expected = 'Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;Integrated Security=SSPI;'  # noqa: E501

    actual = connection_string_helper.build_connection_string(config)

    assert expected == actual


def test_constructing_proper_connection_string_for_sql_server_without_sspi(mocker):  # noqa: E501
    config = configuration.Configuration()
    config.database_integrated_security = ''
    config.database_username = 'userID'
    config.database_password = 'hunter2'

    expected = 'Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;User ID=userID;Password=hunter2;'  # noqa: E501
    actual = connection_string_helper.build_connection_string(config)

    assert expected == actual
