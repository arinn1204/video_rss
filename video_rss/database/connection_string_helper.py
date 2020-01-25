#!.env/bin/python


def build_connection_string(config):
    connection_string = ''
    if config.database_provider == 'mssql':
        connection_string = __build_mssql_connection_string(config)
    return connection_string


def __build_mssql_connection_string(config):
    connection_string = 'Driver={' + config.database_driver + '};'
    connection_string += f"Server={config.database_data_source}"

    if hasattr(config, 'database_instance') is True:
        connection_string += f"\\{config.database_instance}"

    connection_string += ";"
    connection_string += f"Database={config.database_initial_catalog};"

    if config.database_integrated_security == 'SSPI':
        connection_string += "Integrated Security="
        connection_string += f"{config.database_integrated_security};"
    else:
        connection_string += f"UID={config.database_username};"
        connection_string += f"PWD={config.database_password};"
        connection_string += "Authentication=ActiveDirectoryPassword;"

    return connection_string
