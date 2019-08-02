#!/usr/bin/env python

import datetime
import unittest

import trip_packet.trip


TRIP_BASIC = (
    ' E0004    RPT -->06:48                                 FM=01/FA=05  \n'
    ' 1  76C   1886*EWR IAH 0803 1050 M  3:47 1:25                       \n'
    ' 1  76C    748 IAH EWR 1215 1648    3:33        7:20 10:15          \n'
    '                                                MO TU WE TH FR|SA SU\n'
    ' TOTAL CR:  07:20                                               1  2\n'
    ' TOTAL BLK: 07:20                               -- --  5 -- --|-- --\n'
    ' TOTAL DHD: 00:00   TAFB:        10:15          -- -- -- -- --|-- --\n'
    ' TOTAL RIG: 00:00   PER DIEM: $  23.06          -- -- -- -- --|-- --\n'
    ' T/D=  1                                        -- -- -- -- --|-- --\n')

TRIP_HOTEL = (
    ' E0008    RPT -->05:45                                 FM=01/FA=05  \n'
    ' 1  78J    240 EWR LAX 0700 0949    5:49        5:49  7:19  13:26   \n'
    '   HYATT REGENCY AP                  424-702-1234                 F \n'
    ' RPT -->22:15                                                       \n'
    ' 1  77G    415 LAX EWR 2315 0720    5:05        5:05  6:20          \n'
    '                                                MO TU WE TH FR|SA SU\n'
    ' TOTAL CR:  10:54                                               1 --\n'
    ' TOTAL BLK: 10:54                               --  4 -- -- --|-- --\n'
    ' TOTAL DHD: 00:00   TAFB:        25:50          -- -- -- -- --|-- --\n'
    ' TOTAL RIG: 00:00   PER DIEM: $  58.11          -- -- -- -- --|-- --\n'
    ' T/D=  2                                        -- -- -- -- --|-- --\n')

TRIP_SHUTTLE = (
    ' E0019    RPT -->07:20                                 FM=01/FA=05  \n'
    ' 1  76S    363 EWR HNL 0835 1344 M 11:09       11:09 12:39  25:31   \n'
    '   SHERATON KAIULANI                 808-922-5811                 F \n'
    '     VIP LIMO                        808-836-0317                   \n'
    ' RPT -->14:15                                                       \n'
    ' 2  76S    362 HNL EWR 1515 0650 M  9:35        9:35 10:50          \n'
    '                                                MO TU WE TH FR|SA SU\n'
    ' TOTAL CR:  20:44                                               1  2\n'
    ' TOTAL BLK: 20:44                                3  4 -- -- --|-- --\n'
    ' TOTAL DHD: 00:00   TAFB:        47:45          -- -- -- -- --|-- --\n'
    ' TOTAL RIG: 00:00   PER DIEM: $ 107.43          -- -- -- -- --|-- --\n'
    ' T/D=  3                                        -- -- -- -- --|-- --\n')

TRIP_FULL_CALENDAR = (
    ' E0007    RPT -->07:30                                 FM=01/FA=05  \n'
    ' 1  76S   1523*EWR SJU 0845 1241 M  3:56 1:24                       \n'
    ' 1  76S   1173 SJU EWR 1405 1809    4:04        8:00 10:54          \n'
    '                                                MO TU WE TH FR|SA SU\n'
    ' TOTAL CR:  08:00                                              -- --\n'
    ' TOTAL BLK: 08:00                               -- -- --  6  7| 8  9\n'
    ' TOTAL DHD: 00:00   TAFB:        10:54          10 11 12 13 14|15 16\n'
    ' TOTAL RIG: 00:00   PER DIEM: $  24.52          17 18 19 20 21|22 23\n'
    ' T/D=  1                                        24 25 26 27 28|29 30\n')

TRIP_THREE_DAYS = (
    ' E0032    RPT -->15:45                                 FM=01/FA=05  \n'
    ' 1  77Y    598 EWR IAH 1700 1944    3:44        3:44  5:14  14:36   \n'
    '   MARRIOTT AIRPORT                  281-443-2310                 F \n'
    ' RPT -->09:20                                                       \n'
    ' 2  77G   1101 IAH DEN 1020 1147    2:27 1:43                       \n'
    ' 2  77G    313 DEN IAH 1330 1653    2:23        4:50  7:48  17:09   \n'
    '   MARRIOTT AIRPORT                  281-443-2310                 F \n'
    ' RPT -->09:02                                                       \n'
    ' 3  76C   1403*IAH ORD 1002 1240    2:38 3:35                       \n'
    ' 3  77Y   1995 ORD EWR 1615 1940    2:25        5:03  9:53          \n'
    '                                                MO TU WE TH FR|SA SU\n'
    ' TOTAL CR:  15:00                                              -- --\n'
    ' TOTAL BLK: 13:37                               -- -- -- --  7|-- --\n'
    ' TOTAL DHD: 00:00   TAFB:        52:10          -- -- -- -- 14|-- --\n'
    ' TOTAL RIG: 01:23   PER DIEM: $ 117.36          -- -- -- -- --|-- --\n'
    ' T/D=  3                                        -- -- -- -- --|-- --\n')

TRIP_INTL_PHONE = (
    ' E0502    RPT -->07:30                                 FM=01/FA=01   \n'
    ' 1  73G   1063 EWR MEX 0830 1250 M  5:20        5:20  6:50  22:10    \n'
    '   SHERATON MAR ISABELA              525552425555                 D  \n'
    '     SERVISEG S.A.                   521555906201                    \n'
    ' RPT -->10:15                                                        \n'
    ' 2  73G   2252 MEX EWR 1100 1655 M  4:55        4:55  6:10           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  10:15                                               1 -- \n'
    ' TOTAL BLK: 10:15                                3 -- -- -- --|-- -- \n'
    ' TOTAL DHD: 00:00   TAFB:        33:55          10 -- -- -- --|15 -- \n'
    ' TOTAL RIG: 00:00   PER DIEM: $  76.29          -- -- -- -- --|22 -- \n'
    ' T/D=  2                                        -- -- -- -- --|29 -- \n')

TRIP_DH = (
    ' E0022    RPT -->13:45                                 FM=01/FA=05   \n'
    ' 1  20S DH1992*EWR IAD 1430 1604    1:34 1:41                        \n'
    ' 1  77U    340 IAD SFO 1745 2025 M  5:40        5:40  9:55  27:05    \n'
    '   HOLIDAY INN GATEWAY               415-441-4000                 D  \n'
    '     AIRLINE COACH SERVICE           650-697-7733                    \n'
    ' RPT -->22:30                                                        \n'
    ' 2  77G   1796 SFO EWR 2330 0750    5:20        5:20  6:35           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  12:34                                              -- -- \n'
    ' TOTAL BLK: 11:00                               -- -- -- -- --|-- -- \n'
    ' TOTAL DHD: 01:34   TAFB:        42:20          -- -- -- -- --|-- -- \n'
    ' TOTAL RIG: 00:00   PER DIEM: $  95.24          -- -- -- 20 --|-- -- \n'
    ' T/D=  3                                        -- -- -- -- --|-- -- \n')

TRIP_NO_HOUR = (
    ' E0501    RPT -->07:30                                 FM=01/FA=01   \n'
    ' 1  73G   1063*EWR MEX 0830 1250 M  5:20  :55                        \n'
    ' 1  73G   1066 MEX EWR 1345 1940 M  4:55       10:15 12:40           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  10:15                                              -- -- \n'
    ' TOTAL BLK: 10:15                               -- --  5 -- --| 8 -- \n'
    ' TOTAL DHD: 00:00   TAFB:        12:40          -- -- -- -- --|-- -- \n'
    ' TOTAL RIG: 00:00   PER DIEM: $  28.48          -- -- -- -- --|-- -- \n'
    ' T/D=  1                                        -- -- -- -- --|-- -- \n')

TRIP_DHUX = (
    ' E0852    RPT -->09:00                                 FM=01/FA=02   \n'
    ' 1  73Y    746*EWR IAD 1000 1127    1:27 1:18                        \n'
    ' 1    DHUX6201*IAD ATL 1245 1441    1:56 2:14                        \n'
    ' 1  73Y    410 ATL EWR 1655 1918    2:23        3:50 10:33           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  05:46                                              -- -- \n'
    ' TOTAL BLK: 03:50                               -- --  5 -- --|-- -- \n'
    ' TOTAL DHD: 01:56   TAFB:        10:33          -- -- -- -- --|-- -- \n'
    ' TOTAL RIG: 00:00   PER DIEM: $  23.73          -- -- -- -- --|-- -- \n'
    ' T/D=  1                                        -- -- -- -- --|-- -- \n')

TRIP_PHONE_NO_DASH = (
    ' E1104    RPT -->04:00                                 FM=01/FA=02   \n'
    ' 1  20S    244*EWR DEN 0500 0659 M  3:59 1:55                        \n'
    ' 1  37K   1762 DEN SAT 0854 1204    2:10        6:09  9:19  18:08    \n'
    '   HILTON AIRPORT                    2103406060                   F  \n'
    ' RPT -->05:27                                                        \n'
    ' 2  73G    715 SAT EWR 0612 1059    3:47        3:47  4:47           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  10:00                                              -- -- \n'
    ' TOTAL BLK: 09:56                               -- -- --  6 --|-- -- \n'
    ' TOTAL DHD: 00:00   TAFB:        31:14          -- -- -- -- --|-- -- \n'
    ' TOTAL RIG: 00:04   PER DIEM: $  70.26          -- -- -- -- --|-- -- \n'
    ' T/D=  2                                        -- -- -- -- --|-- -- \n')

TRIP_SHUTTLE_NO_PHONE = (
    ' E1196    RPT -->04:45                                 FM=01/FA=02   \n'
    ' 1  75B   1286*EWR DEN 0600 0759 M  3:59 1:39                        \n'
    ' 1  37K    339 DEN SEA 0938 1139    3:01        7:00 10:09  18:26    \n'
    '   HYATT REG LAKE WASH               425-203-1234                 D  \n'
    '     PAX                                                             \n'
    ' RPT -->05:20                                                        \n'
    ' 2  37K   1929 SEA EWR 0605 1420    5:15        5:15  6:15           \n'
    '                                                MO TU WE TH FR|SA SU \n'
    ' TOTAL CR:  12:15                                              -- -- \n'
    ' TOTAL BLK: 12:15                               -- -- -- -- --|-- -- \n'
    ' TOTAL DHD: 00:00   TAFB:        33:50          -- -- -- -- --|-- -- \n'
    ' TOTAL RIG: 00:00   PER DIEM: $  76.11          -- -- -- -- --|-- -- \n'
    ' T/D=  2                                        -- -- -- -- 28|-- -- \n')


class TestEntry(unittest.TestCase):

    def test_parse_trip_str_basic(self):
        """ Verify we can parse the most basic of trips. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_BASIC)
        
        self.assertEqual(trip.trip_str, TRIP_BASIC)
        self.assertEqual(trip.pairing_number, 'E0004')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 1),
                datetime.datetime(2019, 6, 2),
                datetime.datetime(2019, 6, 5)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=7, minutes=20))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=7, minutes=20))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '23.06')

        self.assertEqual(len(trip.turns), 1)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=6, minute=48))
        self.assertEqual(trip.turns[0].hotel_name, None)
        self.assertEqual(trip.turns[0].hotel_phone, None)
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=7, minutes=20))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=10, minutes=15))

        self.assertEqual(len(trip.turns[0].flights), 2)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '76C')
        self.assertEqual(flight.flight_number, '1886')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'IAH')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=3))
        self.assertEqual(flight.time_arrive, datetime.time(hour=10, minute=50))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=47))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=25))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '76C')
        self.assertEqual(flight.flight_number, '748')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'IAH')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=12, minute=15))
        self.assertEqual(flight.time_arrive, datetime.time(hour=16, minute=48))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=3, minutes=33))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_hotel(self):
        """ Verify we can parse a trip with a hotel. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_HOTEL)
        
        self.assertEqual(trip.trip_str, TRIP_HOTEL)
        self.assertEqual(trip.pairing_number, 'E0008')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 1),
                datetime.datetime(2019, 6, 4)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=10, minutes=54))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=10, minutes=54))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=25, minutes=50))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '58.11')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=5, minute=45))
        self.assertEqual(trip.turns[0].hotel_name, 'HYATT REGENCY AP')
        self.assertEqual(trip.turns[0].hotel_phone, '424-702-1234')
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=5, minutes=49))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=7, minutes=19))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=22, minute=15))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=5, minutes=5))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=6, minutes=20))

        self.assertEqual(len(trip.turns[0].flights), 1)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '78J')
        self.assertEqual(flight.flight_number, '240')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'LAX')
        self.assertEqual(flight.time_depart, datetime.time(hour=7, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=9, minute=49))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=5, minutes=49))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=13, minutes=26))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '77G')
        self.assertEqual(flight.flight_number, '415')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'LAX')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=23, minute=15))
        self.assertEqual(flight.time_arrive, datetime.time(hour=7, minute=20))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=5, minutes=5))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_shuttle(self):
        """ Verify we can parse a trip with a shuttle. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_SHUTTLE)
        
        self.assertEqual(trip.trip_str, TRIP_SHUTTLE)
        self.assertEqual(trip.pairing_number, 'E0019')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 1),
                datetime.datetime(2019, 6, 2),
                datetime.datetime(2019, 6, 3),
                datetime.datetime(2019, 6, 4)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=20, minutes=44))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=20, minutes=44))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=47, minutes=45))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '107.43')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=7, minute=20))
        self.assertEqual(trip.turns[0].hotel_name, 'SHERATON KAIULANI')
        self.assertEqual(trip.turns[0].hotel_phone, '808-922-5811')
        self.assertEqual(trip.turns[0].shuttle_name, 'VIP LIMO')
        self.assertEqual(trip.turns[0].shuttle_phone, '808-836-0317')
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=11, minutes=9))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=12, minutes=39))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=14, minute=15))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=9, minutes=35))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=10, minutes=50))

        self.assertEqual(len(trip.turns[0].flights), 1)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '76S')
        self.assertEqual(flight.flight_number, '363')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'HNL')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=35))
        self.assertEqual(flight.time_arrive, datetime.time(hour=13, minute=44))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=11, minutes=9))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=25, minutes=31))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '76S')
        self.assertEqual(flight.flight_number, '362')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'HNL')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=15, minute=15))
        self.assertEqual(flight.time_arrive, datetime.time(hour=6, minute=50))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=9, minutes=35))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_full_calendar(self):
        """ Verify we can parse a trip with a full calendar. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_FULL_CALENDAR)
        
        self.assertEqual(trip.trip_str, TRIP_FULL_CALENDAR)
        self.assertEqual(trip.pairing_number, 'E0007')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, x) for x in range(6, 31)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=8, minutes=0))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=8, minutes=0))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=10, minutes=54))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '24.52')

        self.assertEqual(len(trip.turns), 1)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=7, minute=30))
        self.assertEqual(trip.turns[0].hotel_name, None)
        self.assertEqual(trip.turns[0].hotel_phone, None)
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=8, minutes=0))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=10, minutes=54))

        self.assertEqual(len(trip.turns[0].flights), 2)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '76S')
        self.assertEqual(flight.flight_number, '1523')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'SJU')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=45))
        self.assertEqual(flight.time_arrive, datetime.time(hour=12, minute=41))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=56))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=24))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '76S')
        self.assertEqual(flight.flight_number, '1173')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'SJU')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=14, minute=5))
        self.assertEqual(flight.time_arrive, datetime.time(hour=18, minute=9))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=4, minutes=4))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_three_days(self):
        """ Verify we can parse a trip that is three days long. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_THREE_DAYS)
        
        self.assertEqual(trip.trip_str, TRIP_THREE_DAYS)
        self.assertEqual(trip.pairing_number, 'E0032')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 7),
                datetime.datetime(2019, 6, 14)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=15, minutes=0))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=13, minutes=37))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=52, minutes=10))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=1, minutes=23))
        self.assertEqual(trip.total_per_diem, '117.36')

        self.assertEqual(len(trip.turns), 3)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=15, minute=45))
        self.assertEqual(trip.turns[0].hotel_name, 'MARRIOTT AIRPORT')
        self.assertEqual(trip.turns[0].hotel_phone, '281-443-2310')
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=3, minutes=44))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=5, minutes=14))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=9, minute=20))
        self.assertEqual(trip.turns[1].hotel_name, 'MARRIOTT AIRPORT')
        self.assertEqual(trip.turns[1].hotel_phone, '281-443-2310')
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=4, minutes=50))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=7, minutes=48))

        self.assertEqual(
            trip.turns[2].report_time, datetime.time(hour=9, minute=2))
        self.assertEqual(trip.turns[2].hotel_name, None)
        self.assertEqual(trip.turns[2].hotel_phone, None)
        self.assertEqual(trip.turns[2].shuttle_name, None)
        self.assertEqual(trip.turns[2].shuttle_phone, None)
        self.assertEqual(
            trip.turns[2].time_block, datetime.timedelta(hours=5, minutes=3))
        self.assertEqual(
            trip.turns[2].time_afb, datetime.timedelta(hours=9, minutes=53))

        self.assertEqual(len(trip.turns[0].flights), 1)
        self.assertEqual(len(trip.turns[1].flights), 2)
        self.assertEqual(len(trip.turns[2].flights), 2)

        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '77Y')
        self.assertEqual(flight.flight_number, '598')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'IAH')
        self.assertEqual(flight.time_depart, datetime.time(hour=17, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=19, minute=44))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=44))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=14, minutes=36))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '77G')
        self.assertEqual(flight.flight_number, '1101')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'IAH')
        self.assertEqual(flight.airport_arrive, 'DEN')
        self.assertEqual(flight.time_depart, datetime.time(hour=10, minute=20))
        self.assertEqual(flight.time_arrive, datetime.time(hour=11, minute=47))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=2, minutes=27))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=43))

        flight = trip.turns[1].flights[1]
        self.assertEqual(flight.aircraft_type, '77G')
        self.assertEqual(flight.flight_number, '313')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'DEN')
        self.assertEqual(flight.airport_arrive, 'IAH')
        self.assertEqual(flight.time_depart, datetime.time(hour=13, minute=30))
        self.assertEqual(flight.time_arrive, datetime.time(hour=16, minute=53))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=2, minutes=23))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=17, minutes=9))

        flight = trip.turns[2].flights[0]
        self.assertEqual(flight.aircraft_type, '76C')
        self.assertEqual(flight.flight_number, '1403')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'IAH')
        self.assertEqual(flight.airport_arrive, 'ORD')
        self.assertEqual(flight.time_depart, datetime.time(hour=10, minute=2))
        self.assertEqual(flight.time_arrive, datetime.time(hour=12, minute=40))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=2, minutes=38))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=3, minutes=35))

        flight = trip.turns[2].flights[1]
        self.assertEqual(flight.aircraft_type, '77Y')
        self.assertEqual(flight.flight_number, '1995')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'ORD')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=16, minute=15))
        self.assertEqual(flight.time_arrive, datetime.time(hour=19, minute=40))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=2, minutes=25))
        self.assertEqual(flight.time_layover, None)

    def test_parse_trip_str_intl_phone(self):
        """ Verify we can parse a trip with an international phone. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_INTL_PHONE)
        
        self.assertEqual(trip.trip_str, TRIP_INTL_PHONE)
        self.assertEqual(trip.pairing_number, 'E0502')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 1),
                datetime.datetime(2019, 6, 3),
                datetime.datetime(2019, 6, 10),
                datetime.datetime(2019, 6, 15),
                datetime.datetime(2019, 6, 22),
                datetime.datetime(2019, 6, 29)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=33, minutes=55))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '76.29')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=7, minute=30))
        self.assertEqual(trip.turns[0].hotel_name, 'SHERATON MAR ISABELA')
        self.assertEqual(trip.turns[0].hotel_phone, '525552425555')
        self.assertEqual(trip.turns[0].shuttle_name, 'SERVISEG S.A.')
        self.assertEqual(trip.turns[0].shuttle_phone, '521555906201')
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=5, minutes=20))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=6, minutes=50))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=10, minute=15))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=4, minutes=55))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=6, minutes=10))

        self.assertEqual(len(trip.turns[0].flights), 1)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '73G')
        self.assertEqual(flight.flight_number, '1063')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'MEX')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=30))
        self.assertEqual(flight.time_arrive, datetime.time(hour=12, minute=50))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=5, minutes=20))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=22, minutes=10))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '73G')
        self.assertEqual(flight.flight_number, '2252')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'MEX')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=11, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=16, minute=55))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=4, minutes=55))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_deadhead(self):
        """ Verify we can parse a trip with a dead head leg. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_DH)
        
        self.assertEqual(trip.trip_str, TRIP_DH)
        self.assertEqual(trip.pairing_number, 'E0022')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 20)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=12, minutes=34))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=11, minutes=0))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=1, minutes=34))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=42, minutes=20))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '95.24')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=13, minute=45))
        self.assertEqual(trip.turns[0].hotel_name, 'HOLIDAY INN GATEWAY')
        self.assertEqual(trip.turns[0].hotel_phone, '415-441-4000')
        self.assertEqual(trip.turns[0].shuttle_name, 'AIRLINE COACH SERVICE')
        self.assertEqual(trip.turns[0].shuttle_phone, '650-697-7733')
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=5, minutes=40))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=9, minutes=55))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=22, minute=30))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=5, minutes=20))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=6, minutes=35))

        self.assertEqual(len(trip.turns[0].flights), 2)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '20S')
        self.assertEqual(flight.flight_number, '1992')
        self.assertEqual(flight.dead_head, True)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'IAD')
        self.assertEqual(flight.time_depart, datetime.time(hour=14, minute=30))
        self.assertEqual(flight.time_arrive, datetime.time(hour=16, minute=4))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=1, minutes=34))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=41))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '77U')
        self.assertEqual(flight.flight_number, '340')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'IAD')
        self.assertEqual(flight.airport_arrive, 'SFO')
        self.assertEqual(flight.time_depart, datetime.time(hour=17, minute=45))
        self.assertEqual(flight.time_arrive, datetime.time(hour=20, minute=25))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=5, minutes=40))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=27, minutes=5))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '77G')
        self.assertEqual(flight.flight_number, '1796')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'SFO')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=23, minute=30))
        self.assertEqual(flight.time_arrive, datetime.time(hour=7, minute=50))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=5, minutes=20))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_no(self):
        """ Verify we can parse flight duration with no hour. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_NO_HOUR)
        
        self.assertEqual(trip.trip_str, TRIP_NO_HOUR)
        self.assertEqual(trip.pairing_number, 'E0501')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 5),
                datetime.datetime(2019, 6, 8)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=12, minutes=40))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '28.48')

        self.assertEqual(len(trip.turns), 1)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=7, minute=30))
        self.assertEqual(trip.turns[0].hotel_name, None)
        self.assertEqual(trip.turns[0].hotel_phone, None)
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=10, minutes=15))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=12, minutes=40))

        self.assertEqual(len(trip.turns[0].flights), 2)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '73G')
        self.assertEqual(flight.flight_number, '1063')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'MEX')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=30))
        self.assertEqual(flight.time_arrive, datetime.time(hour=12, minute=50))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=5, minutes=20))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=0, minutes=55))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '73G')
        self.assertEqual(flight.flight_number, '1066')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'MEX')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=13, minute=45))
        self.assertEqual(flight.time_arrive, datetime.time(hour=19, minute=40))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=4, minutes=55))
        self.assertEqual(
            flight.time_layover, None)

    def test_parse_trip_str_dhux(self):
        """ Verify we can parse whatever this DHUX thing is. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_DHUX)
        
        self.assertEqual(trip.trip_str, TRIP_DHUX)
        self.assertEqual(trip.pairing_number, 'E0852')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 5)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=5, minutes=46))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=3, minutes=50))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=1, minutes=56))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=10, minutes=33))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '23.73')

        self.assertEqual(len(trip.turns), 1)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=9, minute=0))
        self.assertEqual(trip.turns[0].hotel_name, None)
        self.assertEqual(trip.turns[0].hotel_phone, None)
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=3, minutes=50))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=10, minutes=33))

        self.assertEqual(len(trip.turns[0].flights), 3)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '73Y')
        self.assertEqual(flight.flight_number, '746')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'IAD')
        self.assertEqual(flight.time_depart, datetime.time(hour=10, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=11, minute=27))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=1, minutes=27))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=18))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '')
        self.assertEqual(flight.flight_number, '6201')
        self.assertEqual(flight.dead_head, True)
        self.assertEqual(flight.airport_depart, 'IAD')
        self.assertEqual(flight.airport_arrive, 'ATL')
        self.assertEqual(flight.time_depart, datetime.time(hour=12, minute=45))
        self.assertEqual(flight.time_arrive, datetime.time(hour=14, minute=41))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=1, minutes=56))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=2, minutes=14))

        flight = trip.turns[0].flights[2]
        self.assertEqual(flight.aircraft_type, '73Y')
        self.assertEqual(flight.flight_number, '410')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'ATL')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=16, minute=55))
        self.assertEqual(flight.time_arrive, datetime.time(hour=19, minute=18))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=2, minutes=23))
        self.assertEqual(flight.time_layover, None)

    def test_parse_trip_str_hotel_phone_no_dash(self):
        """ Verify we can parse a US phone number with no dashes. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_PHONE_NO_DASH)
        
        self.assertEqual(trip.trip_str, TRIP_PHONE_NO_DASH)
        self.assertEqual(trip.pairing_number, 'E1104')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 6),])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=10, minutes=0))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=9, minutes=56))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=31, minutes=14))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=4))
        self.assertEqual(trip.total_per_diem, '70.26')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=4, minute=0))
        self.assertEqual(trip.turns[0].hotel_name, 'HILTON AIRPORT')
        self.assertEqual(trip.turns[0].hotel_phone, '2103406060')
        self.assertEqual(trip.turns[0].shuttle_name, None)
        self.assertEqual(trip.turns[0].shuttle_phone, None)
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=6, minutes=9))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=9, minutes=19))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=5, minute=27))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=3, minutes=47))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=4, minutes=47))

        self.assertEqual(len(trip.turns[0].flights), 2)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '20S')
        self.assertEqual(flight.flight_number, '244')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'DEN')
        self.assertEqual(flight.time_depart, datetime.time(hour=5, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=6, minute=59))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=59))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=55))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '37K')
        self.assertEqual(flight.flight_number, '1762')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'DEN')
        self.assertEqual(flight.airport_arrive, 'SAT')
        self.assertEqual(flight.time_depart, datetime.time(hour=8, minute=54))
        self.assertEqual(flight.time_arrive, datetime.time(hour=12, minute=4))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=2, minutes=10))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=18, minutes=8))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '73G')
        self.assertEqual(flight.flight_number, '715')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'SAT')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=6, minute=12))
        self.assertEqual(flight.time_arrive, datetime.time(hour=10, minute=59))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=3, minutes=47))
        self.assertEqual(flight.time_layover, None)

    def test_parse_trip_str_shuttle_no_phone(self):
        """ Verify we can parse a trip with shuttle with no phone. """
        trip = trip_packet.trip.parse_trip_str(
            datetime.datetime(2019, 6, 1), TRIP_SHUTTLE_NO_PHONE)
        
        self.assertEqual(trip.trip_str, TRIP_SHUTTLE_NO_PHONE)
        self.assertEqual(trip.pairing_number, 'E1196')
        self.assertEqual(trip.days_available, [
                datetime.datetime(2019, 6, 28)])
        
        self.assertEqual(
            trip.total_credit, datetime.timedelta(hours=12, minutes=15))
        self.assertEqual(
            trip.total_block, datetime.timedelta(hours=12, minutes=15))
        self.assertEqual(
            trip.total_deadhead, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(
            trip.total_tafb, datetime.timedelta(hours=33, minutes=50))
        self.assertEqual(
            trip.total_rig, datetime.timedelta(hours=0, minutes=0))
        self.assertEqual(trip.total_per_diem, '76.11')

        self.assertEqual(len(trip.turns), 2)
        self.assertEqual(
            trip.turns[0].report_time, datetime.time(hour=4, minute=45))
        self.assertEqual(trip.turns[0].hotel_name, 'HYATT REG LAKE WASH')
        self.assertEqual(trip.turns[0].hotel_phone, '425-203-1234')
        self.assertEqual(trip.turns[0].shuttle_name, 'PAX')
        self.assertEqual(trip.turns[0].shuttle_phone, '')
        self.assertEqual(
            trip.turns[0].time_block, datetime.timedelta(hours=7, minutes=0))
        self.assertEqual(
            trip.turns[0].time_afb, datetime.timedelta(hours=10, minutes=9))

        self.assertEqual(
            trip.turns[1].report_time, datetime.time(hour=5, minute=20))
        self.assertEqual(trip.turns[1].hotel_name, None)
        self.assertEqual(trip.turns[1].hotel_phone, None)
        self.assertEqual(trip.turns[1].shuttle_name, None)
        self.assertEqual(trip.turns[1].shuttle_phone, None)
        self.assertEqual(
            trip.turns[1].time_block, datetime.timedelta(hours=5, minutes=15))
        self.assertEqual(
            trip.turns[1].time_afb, datetime.timedelta(hours=6, minutes=15))

        self.assertEqual(len(trip.turns[0].flights), 2)
        self.assertEqual(len(trip.turns[1].flights), 1)
        flight = trip.turns[0].flights[0]
        self.assertEqual(flight.aircraft_type, '75B')
        self.assertEqual(flight.flight_number, '1286')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'EWR')
        self.assertEqual(flight.airport_arrive, 'DEN')
        self.assertEqual(flight.time_depart, datetime.time(hour=6, minute=0))
        self.assertEqual(flight.time_arrive, datetime.time(hour=7, minute=59))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=59))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=1, minutes=39))

        flight = trip.turns[0].flights[1]
        self.assertEqual(flight.aircraft_type, '37K')
        self.assertEqual(flight.flight_number, '339')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'DEN')
        self.assertEqual(flight.airport_arrive, 'SEA')
        self.assertEqual(flight.time_depart, datetime.time(hour=9, minute=38))
        self.assertEqual(flight.time_arrive, datetime.time(hour=11, minute=39))
        self.assertEqual(flight.time_total, datetime.timedelta(hours=3, minutes=1))
        self.assertEqual(
            flight.time_layover, datetime.timedelta(hours=18, minutes=26))

        flight = trip.turns[1].flights[0]
        self.assertEqual(flight.aircraft_type, '37K')
        self.assertEqual(flight.flight_number, '1929')
        self.assertEqual(flight.dead_head, False)
        self.assertEqual(flight.airport_depart, 'SEA')
        self.assertEqual(flight.airport_arrive, 'EWR')
        self.assertEqual(flight.time_depart, datetime.time(hour=6, minute=5))
        self.assertEqual(flight.time_arrive, datetime.time(hour=14, minute=20))
        self.assertEqual(
            flight.time_total, datetime.timedelta(hours=5, minutes=15))
        self.assertEqual(
            flight.time_layover, None)


if __name__ == '__main__':
    unittest.main()
