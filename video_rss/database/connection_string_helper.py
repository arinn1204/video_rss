#!env/bin/python


def build_connection_string(config):
    connection_string = ''
    if config.database_provider == 'mssql':
        connection_string = __build_mssql_connection_string(config)
    return connection_string

def __build_mssql_connection_string(config):
    connection_string = 'Driver={' + config.database_driver + '};'
    connection_string += f"Data Source={config.database_data_source}"
    connection_string += f"\\{config.database_instance};" if hasattr(config, 'database_instance') is True else ';'
    connection_string += f"Initial Catalog={config.database_initial_catalog};"
    if config.database_integrated_security == 'SSPI':
        connection_string += f"Integrated Security={config.database_integrated_security};"
    else:
        connection_string += f"User ID={config.database_username};Password={config.database_password};"

    return connection_string
