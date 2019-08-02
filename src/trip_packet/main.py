#!/usr/bin/env python

import sys

import trip_packet.page
import trip_packet.pdf
import trip_packet.trip
        

def main():
    filename = sys.argv[1]
    pdf_reader = trip_packet.pdf.PdfReader(filename)

    for page_num in range(pdf_reader.num_pages()):
        rendered_page = pdf_reader.get_page(page_num)
        page_date, trip_strs = trip_packet.page.parse_trips_from_page(
            rendered_page)

        trip_objs = []
        for idx, trip_str in enumerate(trip_strs):
            try:
                trip = trip_packet.trip.parse_trip_str(page_date, trip_str)
            except Exception as ex:
                import pdb; pdb.set_trace()
            if trip:
                trip_objs.append(trip)

        print('Page {}: {} trips'.format(page_num, len(trip_objs)))


if __name__ == '__main__':
    main()
