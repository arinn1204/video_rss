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
        self.__default_assignment('logging_severity', 'DEBUG', True)
        self.logging_masked_values = ['password', 'key']

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            if attr.upper() in environ:
                self.__dict__[attr] = environ.get(attr.upper())
                return self.__dict__.get(attr)
            else:
                raise AttributeError(f"{attr} does not exist.")

        return self.__dict__.get(attr)

    def __default_assignment(
            self,
            property_name,
            default_value,
            to_upper=False):
        value = default_value
        if property_name.upper() in environ:
            value = environ[property_name.upper()]

        if to_upper:
            value = value.upper()

        if value is not None:
            self.__dict__[property_name] = value
