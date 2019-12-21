#!.env/bin/python

from ...video_rss import configuration


class TestSettingDefaultConfigurations:
    def setup_method(self, method):
        self.config = configuration.Configuration()

    def test_set_no_db_username_by_default(self):
        assert hasattr(self.config, 'database_username') is False

    def test_set_no_db_password_by_default(self):
        assert hasattr(self.config, 'database_password') is False

    def test_set_no_db_instance_by_default(self):
        assert hasattr(self.config, 'database_instance') is False

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
