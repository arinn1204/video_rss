#!.env/bin/python

from ...video_rss import configuration
from ...video_rss.database import connection_string_helper


def test_constructing_proper_connection_string_for_sql_server_with_sspi(mocker):  # noqa: E501
    mocker.patch('sys.platform').return_value = 'Windows'
    config = configuration.Configuration()
    expected = 'Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=noblepanther_test;Trusted_Connection=yes;'  # noqa: E501

    actual = connection_string_helper.build_connection_string(config)

    assert expected == actual


def test_constructing_proper_connection_string_for_sql_server_without_sspi(mocker):  # noqa: E501
    mocker.patch('sys.platform').return_value = 'Windows'
    config = configuration.Configuration()
    config.database_trusted_connection = ''
    config.database_username = 'userID'
    config.database_password = 'hunter2'

    expected = 'Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=noblepanther_test;UID=userID;PWD=hunter2;Authentication=ActiveDirectoryPassword;'  # noqa: E501
    actual = connection_string_helper.build_connection_string(config)

    assert expected == actual
