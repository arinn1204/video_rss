#!.env/bin/python

import json


class Logger:
    def __init__(self, config):
        self.log_level = self.__log_value(config.logging_severity)
        self.build_log = lambda message: self.__build_log(message, config)
        self.masked_values = config.logging_masked_values

    def log(self, message, severity='TRACE'):
        if self.log_level >= self.__log_value(severity):
            log = self.build_log(message)
            formatted_log = json.dumps(log)
            print(formatted_log)

    def __build_log(self, log, config):
        new_log = {
            'message': log
        }
        for key, value in config.__dict__.items():
            section, config_name = key.split('_', 1)

            if section not in new_log:
                new_log[section] = {}

            log_category = new_log[section]

            log_category[config_name] = self.__mask(config_name, value)

        return new_log

    def __mask(self, key, value):
        if key in self.masked_values:
            return '*' * 8
        else:
            return value

    def __log_value(self, level_string):
        levels = {
            'OFF': -1,
            'FATAL': 1,
            'CRITICAL': 2,
            'ERROR': 3,
            'WARNING': 4,
            'DEBUG': 5,
            'TRACE': 6,
            'ALL': 99
        }

        return levels[level_string.upper()]
