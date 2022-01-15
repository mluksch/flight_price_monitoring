import requests

import config


def send_simple_message(subject: str, text: str):
    return requests.post(
        config.MAIL_GUN_ENDPOINT,
        auth=("api", config.MAIL_GUN_API_KEY),
        data={"from": config.MAIL_SENDER,
              "to": [config.MAIL_RECEIVER],
              "subject": subject,
              "text": text})
