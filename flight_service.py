import datetime

import requests

import config


def get_iata_codes_for_city(city_name: str):
    res = requests.get(f"{config.KIWI_API_ENDPOINT}/locations/query", params={
        "location_types": "city",
        "locale": "de-DE",
        "term": city_name,
        "limit": 10,
        "active_only": True
    }, headers={
        "apikey": config.KIWI_API_KEY,
    })
    res.raise_for_status()
    return [item["code"] for item in res.json().get("locations")]


def _format_dt(dt: datetime.datetime) -> str:
    return dt.strftime("%d/%m/%Y")


class Flight:
    def __init__(self, price, routes, utc_departure: str, utc_arrival: str, link: str):
        self.price: float = float(price)
        self.routes: [(str, str)] = routes
        self.utc_departure = utc_departure
        self.utc_arrival = utc_arrival
        self.link = link


def search_for_flights(date_from: datetime.datetime, date_to: datetime.datetime, from_iata: str, to_iata: str):
    res = requests.get(f"{config.KIWI_API_ENDPOINT}/v2/search", params={
        "fly_from": from_iata,
        "fly_to": to_iata,
        "date_from": _format_dt(date_from),
        "only_weekends": False,
        "only_working_days": False,
        "flight_type": "round",
        "curr": "EUR",
        "locale": "de",
        "date_to": _format_dt(date_to),
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "max_stopovers": 3,
        "adults": 2,
        "infants": 0
    }, headers={
        "apikey": config.KIWI_API_KEY
    })
    # res.raise_for_status()
    flights = res.json().get("data")
    return [Flight(price=flight["price"], utc_arrival=flight["utc_arrival"], utc_departure=flight["utc_departure"],
                   routes=flight["routes"], link=flight["deep_link"]) for flight in flights]
