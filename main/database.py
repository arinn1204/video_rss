#!/usr/bin/env python3.8

import pyodbc

class Database:
    def __init__(self, config):
        self.config = config