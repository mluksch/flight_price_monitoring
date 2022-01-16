import datetime
import pprint

import dateutil.relativedelta as r
import numpy

import flight_service
import mail_service
import sheet_service


def check():
    rows = sheet_service.get_flights()
    home_iata = flight_service.get_iata_codes_for_city("Duesseldorf")[0]
    date_from = datetime.datetime.now() + datetime.timedelta(days=1)
    date_to = date_from + r.relativedelta(month=6)
    for row in rows:
        pprint.pprint(row)
        target_iata = row.get("iataCode")
        if not target_iata:
            iata_codes = flight_service.get_iata_codes_for_city(row["city"])
            if len(iata_codes) > 0:
                target_iata = iata_codes[0]

        # search for cheaper flight:
        flight_data = flight_service.search_for_flights(date_from=date_from, date_to=date_to, from_iata=home_iata,
                                                        to_iata=target_iata)
        price_list = [f.price for f in flight_data]
        if len(price_list) > 0:
            min_priced: flight_service.Flight = flight_data[numpy.argmin([f.price for f in flight_data])]
            update_required = not row.get("lowestPrice") or row.get("lowestPrice") > min_priced.price
            if update_required:
                update_set = {"lowestPrice": min_priced.price,
                              "route": ", ".join(
                                  ["->".join(items) for items in
                                   min_priced.routes]),
                              "iataCode": target_iata,
                              "departure": min_priced.utc_departure,
                              "arrival": min_priced.utc_arrival,
                              "link": min_priced.link,
                              "duration": min_priced.duration
                              }
                sheet_service.update_flight(row_id=row["id"], update_set=update_set)
                mail_service.send_flight_price_message(flight=min_priced, home_iata=home_iata,
                                                       target_iata=target_iata)
