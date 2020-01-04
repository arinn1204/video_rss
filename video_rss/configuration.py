#!.env/bin/python

from os import environ


class Configuration:
    def __init__(self):
        self.__default_assignment(
            'database_integrated_security',
            'SSPI')
        self.__default_assignment(
            'database_data_source',
            'localhost')
        self.__default_assignment(
            'database_initial_catalog',
            'noblepanther_test')
        self.__default_assignment(
            'database_provider',
            'mssql')
        self.__default_assignment(
            'database_driver',
            'ODBC Driver 17 for SQL Server')
        self.__default_assignment(
            'database_username',
            None)
        self.__default_assignment(
            'database_password',
            None)
        self.__default_assignment(
            'database_instance',
            None)
        self.__default_assignment('logging_severity', 'DEBUG', True)

    def __default_assignment(
            self,
            property_name,
            default_value,
            to_upper=False):
        value = default_value
        if property_name in environ:
            value = environ[property_name]

        if to_upper:
            value = value.upper()

        if value is not None:
            self.__dict__[property_name] = value
