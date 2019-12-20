#!/usr/bin/env python3.8

import sys,os

from os import environ as ENV

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main'))
import configuration


class TestSettingDbConfigurationsFromEnvironment:
    def setup_method(self, method):
        ENV['database_username'] = 'SA'
        ENV['database_password'] = 'hunter2'
        ENV['database_data_source'] = 'alliseeisstars.database.windows.net'
        ENV['database_initial_catalog'] = 'notenoughmemesintests'
        ENV['database_integrated_security'] = 'NO'
        ENV['database_instance'] = 'int11kf3'
        self.config = configuration.Configuration()

    def teardown_method(self, method):
        self.__delete_if_exist('database_username')
        self.__delete_if_exist('database_password')
        self.__delete_if_exist('database_data_source')
        self.__delete_if_exist('database_initial_catalog')
        self.__delete_if_exist('database_integrated_security')
        self.__delete_if_exist('database_instance')

    def __delete_if_exist(self, key):
        ENV.pop(key, None)

    def test_sets_username_based_on_environment_variable(self):
        assert self.config.database_username == 'SA'

    def test_sets_password_based_on_environment_variable(self):
        assert self.config.database_password == 'hunter2'

    def test_sets_data_source_based_on_environment_variable(self):
        assert self.config.database_data_source == 'alliseeisstars.database.windows.net'

    def test_sets_catalog_based_on_environment_variable(self):
        assert self.config.database_initial_catalog == 'notenoughmemesintests'

    def test_sets_integrated_security_based_on_environment_variable(self):
        assert self.config.database_integrated_security == 'NO'

    def test_sets_instance_based_on_environment_variable(self):
        assert self.config.database_instance == 'int11kf3'

    