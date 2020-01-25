#!.env/bin/python

import os
import re

from ...video_rss import configuration


class TestSettingLoggingConfigurations:
    def teardown_method(self, method):
        for key in os.environ.keys():
            if bool(re.match('^logging', key, re.I)):
                os.environ.pop(key, None)

    def test_sets_default_log_severity_to_debug(self):
        config = configuration.Configuration()

        severity = config.logging_severity

        assert severity == 'DEBUG'

    def test_sets_log_severity_from_environment(self):
        os.environ['LOGGING_SEVERITY'] = 'TRACE'
        config = configuration.Configuration()

        severity = config.logging_severity

        assert severity == 'TRACE'

    def test_sets_log_severity_from_environment_and_sets_to_upper(self):
        os.environ['LOGGING_SEVERITY'] = 'trace'
        config = configuration.Configuration()

        severity = config.logging_severity

        assert severity == 'TRACE'
