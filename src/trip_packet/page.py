#!/usr/bin/env python

import datetime
import re

import trip_packet.util

BASE_REGEX = 'BASE: ----> ([A-Z]+)\s+([A-Z]{3}) ([0-9]{2})-([A-Z]{3}) ([0-9]{2}), ([0-9]{4})'


def parse_trips_from_page(page):
    matches = re.search(BASE_REGEX, page[0])
    if not matches:
        return None, []
    page_date = trip_packet.util.parse_report_date(
        matches.group(6), matches.group(2), matches.group(3))
        
    left_break, right_break = trip_packet.util.find_vertical_breaks(page)

    page_left = []
    page_right = []
    for line in page:
        page_left.append(line[:left_break])
        page_right.append(line[right_break:])
        
    trips = []
    trip_str = ''
    for line in (page_left + page_right):
        if '------' in line:
            trips.append(trip_str)
            trip_str = ''
        else:
            trip_str += '{}\n'.format(line)

    return page_date, trips
