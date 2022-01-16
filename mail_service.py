import requests

import config
import flight_service


def send_simple_message(subject: str, text: str):
    return requests.post(
        config.MAIL_GUN_ENDPOINT,
        auth=("api", config.MAIL_GUN_API_KEY),
        data={"from": config.MAIL_SENDER,
              "to": [config.MAIL_RECEIVER],
              "subject": subject,
              "text": text})


def send_flight_price_message(home_iata: str, target_iata: str, flight: flight_service.Flight):
    send_simple_message(
        f"Cheaper Flight: {home_iata} to {target_iata}for Eur{'{:.2f}'.format(flight.price)}", f"""
    Cheaper Flight detected: {home_iata} to {target_iata}
    Price: Eur{'{:.2f}'.format(flight.price)}
    Departure: {flight.utc_departure}
    Arrival: {flight.utc_arrival}
    Duration: {flight.duration}h
    Link: {flight.link}
    Sheet: {config.SHEET_LINK}
    """)
