#!/usr/bin/env python3.8

import os, sys, uuid, re
import pyodbc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main'))
import configuration
import database

class TestDatabaseConnection:
    
    def setup_method(self, method):
        self.config = configuration.Configuration()
        self.database = database.Database(self.config)

    def teardown_method(self, method):
        [ self.__delete_if_exist(key) for key in os.environ.keys() if bool(re.match('^database', key, re.I)) ]

    def __delete_if_exist(self, key):
        os.environ.pop(key, None)
        return key

    def test_constructing_proper_connection_string_for_sql_server_with_sspi(self, mocker):
        connect_mocker = mocker.Mock()
        mocker.patch('pyodbc.connect', new = connect_mocker)
        db = database.Database(self.config)
        db.get_by_id(str(uuid.uuid4()))
        connect_mocker.assert_called_once_with('Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;Integrated Security=SSPI;')

        
    def test_constructing_proper_connection_string_for_sql_server_without_sspi(self, mocker):
        connect_mocker = mocker.Mock()
        mocker.patch('pyodbc.connect', new = connect_mocker)

        os.environ['database_integrated_security'] = ''
        os.environ['database_username'] = 'userID'
        os.environ['database_password'] = 'hunter2'

        config = configuration.Configuration()
        db = database.Database(config)
        db.get_by_id(str(uuid.uuid4()))

        connect_mocker.assert_called_once_with('Driver={ODBC Driver 17 for SQL Server};Data Source=localhost;Initial Catalog=noblepanther_test;User ID=userID;Password=hunter2;')
