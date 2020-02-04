#!.env/bin/python


def setup_mocks(mocker, fetchall=[(1,)], rowcount=1):
    mocker.patch('sys.platform').return_value = 'Windows'
    mock_pyodbc_connection = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_execute = mocker.Mock()

    mock_pyodbc_connection = mocker.patch('pyodbc.connect')
    mock_pyodbc_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.execute.return_value = mock_execute

    mock_execute.fetchall.return_value = fetchall
    mock_execute.rowcount = rowcount

    return (mock_connection, mock_cursor, mock_execute)
