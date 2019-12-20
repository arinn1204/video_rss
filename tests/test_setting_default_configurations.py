#!/usr/bin/env python3.8

import sys,os

from os import environ as ENV

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'main'))
import configuration

class TestSettingDefaultConfigurations:
    def setup_method(self, method):
        self.config = configuration.Configuration()
        
    def test_set_no_db_username_by_default(self):
        assert hasattr(self.config, 'database_username') == False
    
    def test_set_no_db_password_by_default(self):
        assert hasattr(self.config, 'database_password') == False

    def test_set_no_db_instance_by_default(self):
        assert hasattr(self.config, 'database_instance') == False

    def test_set_db_provider_by_default(self):
        assert self.config.database_provider == 'mssql'

    def test_set_integrated_security_to_sspi_by_default(self):
        assert self.config.database_integrated_security == 'SSPI'

    def test_set_data_source_to_localhost_by_default(self):
        assert self.config.database_data_source == 'localhost'

    def test_set_initial_catalog_to_noblepanther_test_by_default(self):
        assert self.config.database_initial_catalog == 'noblepanther_test'
        
    def test_set_driver_by_default(self):
        assert self.config.database_driver == 'ODBC Driver 17 for SQL Server'
    