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
