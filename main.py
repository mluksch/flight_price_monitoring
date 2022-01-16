import datetime
import pprint

import dateutil.relativedelta as r
import numpy

import flight_service
import sheet_service

rows = sheet_service.get_flights()

HOME_IATA = flight_service.get_iata_codes_for_city("Duesseldorf")[0]

date_from = datetime.datetime.now() + datetime.timedelta(days=1)
date_to = date_from + r.relativedelta(month=6)

for row in rows:
    pprint.pprint(row)
    # update iata column:
    if not row["iataCode"]:
        iata_codes = flight_service.get_iata_codes_for_city(row["iataCode"])
        if len(iata_codes) > 0:
            to_iata = iata_codes[0]
            sheet_service.update_flight(row_id=row["id"], update_set={"iataCode": to_iata})

    # search for cheaper flight:
    flight_data = flight_service.search_for_flights(date_from=date_from, date_to=date_to, from_iata=HOME_IATA,
                                                    to_iata=row["iataCode"])
    price_list = [f.price for f in flight_data]
    if len(price_list) > 0:
        min_priced: flight_service.Flight = flight_data[numpy.argmin([f.price for f in flight_data])]
        update_required = not row.get("lowestPrice") or row.get("lowestPrice") > min_priced.price
        if update_required:
            updated = sheet_service.update_flight(row_id=row["id"], update_set={"lowestPrice": min_priced.price,
                                                                                "route": ", ".join(
                                                                                    ["->".join(items) for items in
                                                                                     min_priced.routes]),
                                                                                "departure": min_priced.utc_departure,
                                                                                "arrival": min_priced.utc_arrival,
                                                                                "link": min_priced.link
                                                                                })
            pprint.pprint(f"updated: {updated}")
