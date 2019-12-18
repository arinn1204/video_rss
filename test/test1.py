#!/usr/bin/env python3.8

import unittest
from unittest import mock

class TestClass(unittest.TestCase):
    def test_passing_test(self):
        self.assertEqual(1, 1)

    def test_failing_test(self):
        self.assertTrue(True)

