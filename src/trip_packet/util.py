#!/usr/bin/env python

import datetime

MONTH_MAP = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 
    'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10,
    'NOV': 11, 'DEC': 12}


def parse_time(time_str):
    """ Convert the string representation of a time into a 
    datetime object.  This expects the time to be in one of two
    formats:
      HHMM
      HH:MM
    """
    if ':' in time_str:
        hours, minutes = time_str.split(':')
    else:
        hours = int(time_str[:2])
        minutes = int(time_str[2:])

    return datetime.time(int(hours), int(minutes))

def parse_duration(duration_str):
    """ Convert the string representation of a duration into a 
    timedelta object.  This expects the duration to be in one of two
    formats:
      HH:MM
      :55
    """
    if duration_str[0] == ':':
        hours = 0
        minutes = duration_str[1:]
    else:
        hours, minutes = duration_str.split(':')
    return datetime.timedelta(hours=int(hours), minutes=int(minutes))

def parse_report_date(year, month, day):
    """ do something """
    return datetime.datetime(
        year=int(year), month=MONTH_MAP[month], day=int(day))

def find_vertical_breaks(lines):
    """ Given a list of strings find the position of the largest vertical
    break.  A vertical break is a column that is blank in the same 
    position in each of the lines.
    """
    max_width = max([len(x) for x in lines])

    split_cols = []
    for col in range(max_width):
        for line in lines:
            if col < len(line) and line[col] != ' ':
                col = None
                break

        if col:
            split_cols.append(col)

    largest_series = []
    series_start = 0
    for idx, col in enumerate(split_cols):
        if idx == 0:
            continue
        
        if split_cols[idx-1] == col - 1:
            if len(largest_series) <= idx - series_start:
                largest_series = split_cols[series_start:idx+1]
        else:
            series_start = idx

    return min(largest_series), max(largest_series)
