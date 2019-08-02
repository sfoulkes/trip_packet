#!/usr/bin/env python

import datetime
import unittest

import trip_packet.util


class TestUtil(unittest.TestCase):

    def test_parse_time(self):
        """ Verify we correctly parse the time. """
        self.assertEqual(
            trip_packet.util.parse_time('09:15'),
            datetime.time(hour=9, minute=15))
        self.assertEqual(
            trip_packet.util.parse_time('0915'),
            datetime.time(hour=9, minute=15))

    def test_parse_duration(self):
        """ Verify we correctly parse a duration. """
        self.assertEqual(
            trip_packet.util.parse_duration('09:15'),
            datetime.timedelta(hours=9, minutes=15))
        self.assertEqual(
            trip_packet.util.parse_duration(':55'),
            datetime.timedelta(hours=0, minutes=55))



if __name__ == '__main__':
    unittest.main()
