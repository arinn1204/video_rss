#!.env/bin/python

from ...video_rss import configuration
from ...video_rss.logging.logger import Logger


def test_should_pass_log_object_to_json_converter(mocker):
    config = configuration.Configuration()
    config.__dict__.clear()
    config.logging_severity = 'TRACE'
    config.logging_masked_values = ['password', 'key']

    log_object = {
        'username': 'hunter2',
        'password': '***'
    }

    expected_result = {
        'message': {
            'username': 'hunter2',
            'password': '***'
        },
        'logging': {
            'severity': 'TRACE',
            'masked_values': ['password', 'key']
        }
    }

    json_mock = mocker.patch('json.dumps')
    logger = Logger(config)

    logger.log(log_object)

    json_mock.assert_called_once_with(expected_result)


def test_should_mask_database_password(mocker):
    config = configuration.Configuration()
    config.__dict__.clear()
    config.logging_severity = 'TRACE'
    config.database_password = 'hunter2'
    config.logging_masked_values = ['password']

    log_object = "some log message oh no!"

    expected_result = {
        'message': "some log message oh no!",
        'logging': {
            'severity': 'TRACE',
            'masked_values': ['password']
        },
        'database': {
            'password': '********'
        }
    }

    json_mock = mocker.patch('json.dumps')
    logger = Logger(config)

    logger.log(log_object)

    json_mock.assert_called_once_with(expected_result)


def test_should_mask_api_key(mocker):
    config = configuration.Configuration()
    config.__dict__.clear()
    config.logging_severity = 'TRACE'
    config.someapi_key = 'hunter2'
    config.logging_masked_values = ['key']

    log_object = "some log message oh no!"

    expected_result = {
        'message': "some log message oh no!",
        'logging': {
            'severity': 'TRACE',
            'masked_values': ['key']
        },
        'someapi': {
            'key': '********'
        }
    }

    json_mock = mocker.patch('json.dumps')
    logger = Logger(config)

    logger.log(log_object)

    json_mock.assert_called_once_with(expected_result)


def test_should_not_log_if_below_threshold(mocker):
    config = configuration.Configuration()
    config.__dict__.clear()
    config.logging_severity = 'WARNING'
    config.logging_masked_values = ['key', 'password']

    log_object = "some log message oh no!"

    json_mock = mocker.patch('json.dumps')
    logger = Logger(config)

    logger.log(log_object, 'TRACE')

    json_mock.assert_not_called()
