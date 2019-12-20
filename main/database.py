#!/usr/bin/env python3.8

import pyodbc

class Database:
    def __init__(self, config):
        self.config = config

    def get_by_id(self, id):
        connection = self.__get_connection()

    def __get_connection(self):
        connection_string = self.__build_connection_string(self.config)

        return pyodbc.connect(connection_string)

    def __build_connection_string(self, config):
        if config.database_provider == 'mssql':
            return self.__build_mssql_connection_string(config)

    def __build_mssql_connection_string(self, config):
        connection_string = 'Driver={' + config.database_driver + '};'
        connection_string += f"Data Source={config.database_data_source}"
        connection_string += f"\\{config.database_instance};" if hasattr(config, 'database_instance') == True else ';'
        connection_string += f"Initial Catalog={config.database_initial_catalog};"
        if config.database_integrated_security == 'SSPI':
            connection_string += f"Integrated Security={config.database_integrated_security};"
        else:
            connection_string += f"User ID={config.database_username};Password={config.database_password};"

        return connection_string