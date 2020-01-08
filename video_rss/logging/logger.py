#!.env/bin/python

import json


class Logger:
    def __init__(self, config):
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
        self.log_level = levels[config.logging_severity]
        self.build_log = lambda message: self.__build_log(message, config)
        self.masked_values = config.logging_masked_values

    def log_trace(self, log):
        if self.log_level >= 6:
            self.__log(log)

    def __log(self, message):
        log = self.build_log(message)
        formatted_log = json.dumps(log)
        print(formatted_log)

    def __build_log(self, log, config):
        new_log = {
            'message': log
        }
        for key, value in config.__dict__.items():
            config_sections = key.split('_', 1)
            category = config_sections[0]
            config_value = config_sections[1]

            if category not in new_log:
                new_log[category] = {}

            log_category = new_log[category]

            log_category[config_value] = self.__mask(config_value, value)

        return new_log

    def __mask(self, key, value):
        if key in self.masked_values:
            return '*' * 8
        else:
            return value
