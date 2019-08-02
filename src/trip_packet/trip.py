#!/usr/bin/env python

import re

import trip_packet.data_structures
import trip_packet.util

REPORT_REGEX = 'RPT -->([0-9]{2}:[0-9]{2})'
REPORT_FIRST_REGEX = '(E[0-9]{4})\s+RPT -->([0-9]{2}:[0-9]{2})'
FLIGHT_REGEX = '\s*(\d)\s+([0-9A-Z]*)\s+([DH|DHUX]*)\s*([0-9]+)([\*]*)\s*([A-Z]+)\s+([A-Z]+)\s+([0-9]{4})\s+([0-9]{4})\s+([M]*)\s+([0-9\:]+)\s+([0-9\:]+)'
FLIGHT_LAST_REGEX = '\s*(\d)\s+([0-9A-Z]*)\s+([DH|DHUX]*)\s*([0-9]+)([\*]*)\s*([A-Z]+)\s+([A-Z]+)\s+([0-9]{4})\s+([0-9]{4})\s+([M]*)\s+([0-9\:]+)\s+([0-9\:]+)\s+([0-9\:]+)'
FLIGHT_LAST_LAYOVER_REGEX = '\s*(\d)\s+([0-9A-Z]*)\s+([DH|DHUX]*)\s*([0-9]+)([\*]*)\s*([A-Z]+)\s+([A-Z]+)\s+([0-9]{4})\s+([0-9]{4})\s+([M]*)\s+([0-9\:]+)\s+([0-9\:]+)\s+([0-9\:]+)\s+([0-9\:]+)'
HOTEL_REGEX = '  \s*([A-Z \.]+)\s+([0-9\-]*)\s+([FD])'
SHUTTLE_REGEX = '    \s*([A-Z \.]+)\s+([0-9\-]*)\s+'
CALENDAR_REGEX = 'MO TU WE TH FR|SA SU'

TOTAL_CR_REGEX = 'TOTAL CR:\s*([0-9]+\:[0-9]{2})'
TOTAL_BLK_REGEX = 'TOTAL BLK:\s*([0-9]+\:[0-9]{2})'
TOTAL_DHD_REGEX = 'TOTAL DHD:\s*([0-9]+\:[0-9]{2})'
TOTAL_RIG_REGEX = 'TOTAL RIG:\s*([0-9]+\:[0-9]{2})'
TOTAL_TAFB_REGEX = 'TAFB:\s*([0-9]+\:[0-9]{2})'
TOTAL_PER_DIEM_REGEX = 'PER DIEM:\s*\$\s*([0-9]+\.[0-9]{2})'

                             
def build_flight(trip, matches):
    # 1  77Y   1162*EWR ORD 0735 0905    2:30 2:25
    flight = trip_packet.data_structures.Flight()
    trip.turns[-1].flights.append(flight)
    flight.aircraft_type = matches.group(2)
    flight.dead_head = True if matches.group(3) else False
    flight.flight_number = matches.group(4)
    flight.airport_depart = matches.group(6)
    flight.airport_arrive = matches.group(7)
    flight.time_depart = trip_packet.util.parse_time(matches.group(8))
    flight.time_arrive = trip_packet.util.parse_time(matches.group(9))
    flight.time_total = trip_packet.util.parse_duration(matches.group(11))
    flight.time_layover = trip_packet.util.parse_duration(matches.group(12))

def build_last_flight(trip, matches):
    # 1  20S DH 609 ORD EWR 1130 1447    2:17        2:30  8:27
    # self.time_block = None
    # self.time_afb = None
    flight = trip_packet.data_structures.Flight()
    trip.turns[-1].flights.append(flight)
    flight.aircraft_type = matches.group(2)
    flight.dead_head = True if matches.group(3) else False
    flight.flight_number = matches.group(4)
    flight.airport_depart = matches.group(6)
    flight.airport_arrive = matches.group(7)
    flight.time_depart = trip_packet.util.parse_time(matches.group(8))
    flight.time_arrive = trip_packet.util.parse_time(matches.group(9))
    flight.time_total = trip_packet.util.parse_duration(matches.group(11))

    trip.turns[-1].time_block = trip_packet.util.parse_duration(matches.group(12))
    trip.turns[-1].time_afb = trip_packet.util.parse_duration(matches.group(13))

def build_last_flight_layover(trip, matches):
    #  1  78J    240 EWR LAX 0700 0949    5:49        5:49  7:19  13:26
    # self.time_block = None
    # self.time_afb = None
    flight = trip_packet.data_structures.Flight()
    trip.turns[-1].flights.append(flight)
    flight.aircraft_type = matches.group(2)
    flight.dead_head = True if matches.group(3) else False
    flight.flight_number = matches.group(4)
    flight.airport_depart = matches.group(6)
    flight.airport_arrive = matches.group(7)
    flight.time_depart = trip_packet.util.parse_time(matches.group(8))
    flight.time_arrive = trip_packet.util.parse_time(matches.group(9))
    flight.time_total = trip_packet.util.parse_duration(matches.group(11))
    flight.time_layover = trip_packet.util.parse_duration(matches.group(14))

    trip.turns[-1].time_block = trip_packet.util.parse_duration(matches.group(12))
    trip.turns[-1].time_afb = trip_packet.util.parse_duration(matches.group(13))

def parse_total(trip, lines):
    for line in lines:
        matches = re.search(TOTAL_CR_REGEX, line)
        if matches:
            trip.total_credit = trip_packet.util.parse_duration(matches.group(1))
            continue
        matches = re.search(TOTAL_BLK_REGEX, line)
        if matches:
            trip.total_block = trip_packet.util.parse_duration(matches.group(1))
            continue
        matches = re.search(TOTAL_DHD_REGEX, line)
        if matches:
            trip.total_deadhead = trip_packet.util.parse_duration(matches.group(1))
            matches = re.search(TOTAL_TAFB_REGEX, line)
            trip.total_tafb = trip_packet.util.parse_duration(matches.group(1))
            continue
        matches = re.search(TOTAL_RIG_REGEX, line)
        if matches:
            trip.total_rig = trip_packet.util.parse_duration(matches.group(1))
            matches = re.search(TOTAL_PER_DIEM_REGEX, line)
            trip.total_per_diem = matches.group(1)
            continue

def parse_calendar(trip, report_date, lines):
    _, cal_start = trip_packet.util.find_vertical_breaks(lines)
    for line in lines[1:]:
        just_dates = line[cal_start + 1:].replace('-', ' ').replace('|', ' ')
        for a_date in just_dates.split():
            trip.days_available.append(report_date.replace(day=int(a_date)))

def parse_trip_str(report_date, trip_str):
    lines = trip_str.splitlines()
    if not lines:
        return None
    matches = re.search(REPORT_FIRST_REGEX, lines[0])
    if not matches:
        return None

    trip = trip_packet.data_structures.Trip(trip_str, matches.group(1))
    trip.add_turn(trip_packet.data_structures.Turn(
            trip_packet.util.parse_time(matches.group(2))))

    for idx, line in enumerate(lines[1:]):
        matches = re.search(FLIGHT_LAST_LAYOVER_REGEX, line)        
        if matches:
            build_last_flight_layover(trip, matches)
            continue
        matches = re.search(FLIGHT_LAST_REGEX, line)        
        if matches:
            build_last_flight(trip, matches)
            continue
        matches = re.search(FLIGHT_REGEX, line)
        if matches:
            build_flight(trip, matches)
            continue
        matches = re.search(REPORT_REGEX, line)
        if matches:
            trip.add_turn(trip_packet.data_structures.Turn(
                    trip_packet.util.parse_time(matches.group(1))))
            continue
        matches = re.search(CALENDAR_REGEX, line)
        if matches:
            parse_total(trip, lines[idx + 1:])
            parse_calendar(trip, report_date, lines[idx + 1:])
            break
        matches = re.search(HOTEL_REGEX, line)
        if matches:
            last_turn = trip.get_last_turn()
            last_turn.hotel_name = matches.group(1).strip()
            last_turn.hotel_phone = matches.group(2)
            continue
        matches = re.search(SHUTTLE_REGEX, line)
        if matches:
            last_turn = trip.get_last_turn()            
            last_turn.shuttle_name = matches.group(1).strip()
            last_turn.shuttle_phone = matches.group(2)
            continue
        else:
            import pdb; pdb.set_trace()
    
    return trip
