import pprint

import flight_service
import sheet_service

flights = sheet_service.get_flights()

for flight in flights:
    pprint.pprint(flights)
    iata_codes = flight_service.get_iata_codes_for_city(flight["city"])
    if len(iata_codes) > 0:
        sheet_service.update_flight(row_id=flight["id"], update_set={"iataCode": iata_codes[0]})
