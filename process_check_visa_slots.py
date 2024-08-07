import json
import requests
import logging
import pytz
from datetime import datetime

SLOTS_URL = "https://app.checkvisaslots.com/slots/v3"
CHROME_EXT = "chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
VERSION = "4.5.5"

logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)


def convert_to_pst(timestamp_string):
  """Converts a GMT timestamp string to PST.

  Args:
    timestamp_string: The timestamp string in the format 'Wed, 07 Aug 2024 02:30:42 GMT'.

  Returns:
    The timestamp converted to PST as a datetime object.
  """

  # Parse the timestamp string into a datetime object with GMT timezone
  gmt_datetime = datetime.strptime(timestamp_string, '%a, %d %b %Y %H:%M:%S GMT')
  gmt_timezone = pytz.timezone('GMT')
  gmt_aware_datetime = gmt_timezone.localize(gmt_datetime)

  # Convert the datetime object to PST
  pst_timezone = pytz.timezone('America/Los_Angeles')
  pst_aware_datetime = gmt_aware_datetime.astimezone(pst_timezone)

  # Format the PST datetime in 12h format
  pst_datetime_str = pst_aware_datetime.strftime('%a, %d %b %Y %I:%M:%S %p')

  return pst_datetime_str


def check_consulate(results, consulate="CHENNAI"):
    for result in results:
        if consulate in result["visa_location"]:
            return result["slots"], convert_to_pst(result["createdon"])


def fetch_check_visa_slots(access_token):
    headers = {
        'origin': CHROME_EXT,
        'user-agent': UA,
        'x-api-key': access_token,
        'Extversion': VERSION,
    }
    response = requests.get(SLOTS_URL, headers=headers)
    if response.ok:
        # print(response.text)
        return response.json()['slotDetails']
    return None


def process_check_visa_slots(access_token):
    json_response = fetch_check_visa_slots(access_token)
    if json_response:
        slot_count, timestamp = check_consulate(json_response)
        if slot_count != 0:
            logging.info(f"Found {slot_count} slots at time: {timestamp}")
            return f"Found **{slot_count}** slots at **{timestamp}**"
    return None


if __name__ == '__main__':
    print(process_check_visa_slots("NBHZEV"))
