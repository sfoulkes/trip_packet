#!/usr/bin/env python


class Flight():
    
    def __init__(self):
        self.aircraft_type = None
        self.flight_number = None
        self.dead_head = False
        self.airport_depart = None
        self.airport_arrive = None
        self.time_depart = None
        self.time_arrive = None
        self.time_total = None
        self.time_layover = None

    def __repr__(self):
        data = ''
        data += '{} {} {}'.format(
            self.aircraft_type, self.flight_number, self.dead_head)
        data += ' {} {}\n'.format(self.airport_arrive, self.airport_depart)
        data += '      Depart: {} Arrive: {} Layover: {}\n'.format(
            self.time_depart, self.time_arrive, self.time_layover)
        return data

class Turn():

    def __init__(self, report_time):
        self.report_time = report_time

        self.flights = []
        self.hotel_name = None
        self.hotel_phone = None
        self.shuttle_name = None
        self.shuttle_phone = None
        self.time_block = None
        self.time_afb = None

    def __repr__(self):
        data = ''
        data += '  Report: {} AFB: {} Block: {}\n'.format(
            self.report_time, self.time_afb, self.time_block)
        data += '    Hotel: {} {}\n'.format(
            self.hotel_name, self.hotel_phone)
        data += '    Shuttle: {} {}\n'.format(
            self.shuttle_name, self.shuttle_phone)
        for flight in self.flights:
            data += '    {}'.format(flight)
        return data

class Trip():

    def __init__(self, trip_str, pairing_number):
        self.trip_str = trip_str
        self.pairing_number = pairing_number

        self.turns = []
        self.days_available = []
        self.total_credit = None
        self.total_block = None
        self.total_deadhead = None
        self.total_tafb = None
        self.total_rig = None
        self.total_per_diem = None

    def add_turn(self, turn):
        self.turns.append(turn)

    def get_last_turn(self):
        return self.turns[-1]

    def __repr__(self):
        data = ''
        data += 'Paring Number: {}\n'.format(self.pairing_number)
        data += '  CR: {} BLK: {} DHD: {} TAFB: {}\n'.format(
            self.total_credit, self.total_block, self.total_deadhead,
            self.total_tafb)
        data += '  RIG: {} PER DIEM: {}\n'.format(
            self.total_rig, self.total_per_diem)
        data += 'Days Available:\n'
        for day_available in self.days_available:
            data += '  {}\n'.format(day_available)
        data += 'Turns:\n'
        for turn in self.turns:
            data += '{}\n'.format(turn)

        return data
