import json
import requests
import logging

URL = "https://app.checkvisaslots.com/slots/v1"
CHROME_EXT = "chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl"
UA = "user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)


def fetch_check_visa_slots(access_token):
    headers = dict()
    headers['origin'] = CHROME_EXT
    headers['user-agent'] = UA
    headers['x-api-key'] = access_token
    response = requests.get(URL, headers=headers)
    if response.ok:
        return response.json()['slotDetails']
    return None


def process_check_visa_slots(access_token):
    json_response = fetch_check_visa_slots(access_token)
    result = []
    if json_response:
        for slot_details in json_response:
            slots = slot_details.get('slots')
            location = slot_details.get('visa_location').split()[-2]
            if slots != 0:
                logging.info(f"Found {slots} slots at {location}")
                result.append(f"Found **{slots}** slots at **{location}**")
    return "\n".join(result)


if __name__ == '__main__':
    print(process_check_visa_slots("TOKEN"))
