import requests

import config


def get_flights():
    res = requests.get(config.SHEETY_ENDPOINT, headers={
        "Authorization": f"Bearer {config.SHEETY_API_KEY}"
    })
    res.raise_for_status()
    result: dict = res.json()
    return result.get("prices")


def update_flight(row_id: int, update_set: dict):
    res = requests.put(f"{config.SHEETY_ENDPOINT}/{row_id}", headers={
        "Authorization": f"Bearer {config.SHEETY_API_KEY}"
    }, json={"price": update_set})
    res.raise_for_status()
    result: dict = res.json()
    return result.get("prices")
    d
