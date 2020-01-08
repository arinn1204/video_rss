#!.env/bin/python

from ...video_rss import configuration
from ...video_rss.logging.logger import Logger


class TestLogger:

    def setup_method(self, method):
        self.config = configuration.Configuration()
        self.config.logging_severity = 'TRACE'

    def test_should_pass_log_object_to_json_converter(self, mocker):
        self.config.__dict__.clear()
        self.config.logging_severity = 'TRACE'
        self.config.logging_masked_values = ['password', 'key']

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
        logger = Logger(self.config)

        logger.log_trace(log_object)

        json_mock.assert_called_once_with(expected_result)

    def test_should_mask_database_password(self, mocker):
        self.config.__dict__.clear()
        self.config.logging_severity = 'TRACE'
        self.config.database_password = 'hunter2'
        self.config.logging_masked_values = ['password']

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
        logger = Logger(self.config)

        logger.log_trace(log_object)

        json_mock.assert_called_once_with(expected_result)

    def test_should_mask_api_key(self, mocker):
        self.config.__dict__.clear()
        self.config.logging_severity = 'TRACE'
        self.config.someapi_key = 'hunter2'
        self.config.logging_masked_values = ['key']

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
        logger = Logger(self.config)

        logger.log_trace(log_object)

        json_mock.assert_called_once_with(expected_result)

    def test_should_not_log_if_below_threshold(self, mocker):
        self.config.logging_severity = 'OFF'

        log_object = "some log message oh no!"

        json_mock = mocker.patch('json.dumps')
        logger = Logger(self.config)

        logger.log_trace(log_object)

        json_mock.assert_not_called()
