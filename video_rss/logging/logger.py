#!.env/bin/python


class Logger:
    def __init__(self, config):
        levels = {
            1: 'TRACE',
            2: 'DEBUG',
            3: 'WARNING',
            4: 'ERROR',
            5: 'CRITICAL',
            6: 'FATAL'
        }
        self.log_level = levels[config.logging_severity]

    def log_trace(self, log):
        if self.log_level <= 1:
            self.__log(log)

    def __log(self, log):
        pass
