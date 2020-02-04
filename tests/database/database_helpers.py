#!.env/bin/python


def setup_mocks(mocker):
    mocker.patch('sys.platform').return_value = 'Windows'
    mock_pyodbc_connection = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_execute = mocker.Mock()

    mock_pyodbc_connection = mocker.patch('pyodbc.connect')
    mock_pyodbc_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = mock_execute
    mock_execute.fetchall.return_value = [(1,)]
    mock_execute.rowcount = 1

    return (mock_connection, mock_cursor, mock_execute)
