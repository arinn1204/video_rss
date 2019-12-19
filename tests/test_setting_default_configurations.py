#!/usr/bin/env python3.8

import sys,os

from os import environ as ENV

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main'))
import configuration

class TestSettingDefaultConfigurations:
    def setup_method(self, method):
        self.config = configuration.Configuration()

    def teardown_method(self, method):
        self.__delete_if_exist('db_username')
        self.__delete_if_exist('db_password')
        self.__delete_if_exist('db_source')
        self.__delete_if_exist('db_catalog')

    def __delete_if_exist(self, key):
        ENV.pop(key, None)

    def test_set_no_db_username_by_default(self):
        assert hasattr(self.config, 'db_username') == False
    
    def test_set_no_db_password_by_default(self):
        assert hasattr(self.config, 'db_password') == False

    def test_set_no_db_instance_by_default(self):
        assert hasattr(self.config, 'db_instance') == False

    def test_set_integrated_security_to_sspi_by_default(self):
        assert self.config.integrated_security == 'SSPI'

    def test_set_data_source_to_localhost_by_default(self):
        assert self.config.data_source == 'localhost'

    def test_set_initial_catalog_to_noblepanther_test_by_default(self):
        assert self.config.initial_catalog == 'noblepanther_test'
    