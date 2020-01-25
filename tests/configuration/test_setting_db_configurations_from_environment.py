#!.env/bin/python

import re

from os import environ as ENV

from ...video_rss import configuration


class TestSettingDbConfigurationsFromEnvironment:
    def setup_method(self, method):
        ENV['DATABASE_USERNAME'] = 'SA'
        ENV['DATABASE_PASSWORD'] = 'hunter2'
        ENV['DATABASE_DATA_SOURCE'] = 'alliseeisstars.database.windows.net'
        ENV['DATABASE_INITIAL_CATALOG'] = 'notenoughmemesintests'
        ENV['DATABASE_INTEGRATED_SECURITY'] = 'NO'
        ENV['DATABASE_INSTANCE'] = 'int11kf3'
        ENV['DATABASE_PROVIDER'] = 'postgres'
        ENV['DATABASE_DRIVER'] = 'ODBC Driver 14 for SQL Server'
        self.config = configuration.Configuration()

    def teardown_method(self, method):
        for key in ENV.keys():
            if bool(re.match('^DATABASE', key, re.I)):
                self.__delete_if_exist(key)

    def __delete_if_exist(self, key):
        ENV.pop(key, None)
        return key

    def test_sets_username_based_on_environment_variable(self):
        assert self.config.database_username == 'SA'

    def test_sets_password_based_on_environment_variable(self):
        assert self.config.database_password == 'hunter2'

    def test_sets_data_source_based_on_environment_variable(self):
        expected_data_source = 'alliseeisstars.database.windows.net'
        assert self.config.database_data_source == expected_data_source

    def test_sets_catalog_based_on_environment_variable(self):
        assert self.config.database_initial_catalog == 'notenoughmemesintests'

    def test_sets_integrated_security_based_on_environment_variable(self):
        assert self.config.database_integrated_security == 'NO'

    def test_sets_instance_based_on_environment_variable(self):
        assert self.config.database_instance == 'int11kf3'

    def test_sets_provider_based_on_environment_variable(self):
        assert self.config.database_provider == 'postgres'

    def test_sets_driver_based_on_environment_variable(self):
        for key in ENV.keys():
            if bool(re.match('^DATABASE', key, re.I)):
                print(key, ENV[key])
        import json

        print(json.dumps(self.config.__dict__))
        assert self.config.database_driver == 'ODBC Driver 14 for SQL Server'
