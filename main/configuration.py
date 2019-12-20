#!/usr/bin/env python3.8

from os import environ

class Configuration:
    def __init__(self):
        self.__default_assignment('database_integrated_security', 'SSPI')
        self.__default_assignment('database_data_source', 'localhost')
        self.__default_assignment('database_initial_catalog', 'noblepanther_test')
        self.__default_assignment('database_username', None)
        self.__default_assignment('database_password', None)
        self.__default_assignment('database_instance', None)
        self.__default_assignment('database_provider', None)


    def __default_assignment(self, property_name, default_value):
        if property_name in environ:
            self.__dict__[property_name] = environ[property_name]
        elif default_value is not None:
            self.__dict__[property_name] = default_value
        