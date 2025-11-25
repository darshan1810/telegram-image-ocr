"""
Visa slots availability checker.
"""
from typing import Optional, Tuple
import json
import logging

import requests
import pytz
from datetime import datetime

import config


class VisaSlotsChecker:
    """Checks for available visa appointment slots."""

    def __init__(
        self,
        api_url: str = config.SLOTS_URL,
        user_agent: str = config.USER_AGENT,
        consulate: str = config.DEFAULT_CONSULATE,
    ):
        """
        Initialize visa slots checker.
        
        Args:
            api_url: API endpoint URL
            user_agent: User agent string
            consulate: Target consulate location
        """
        self.api_url = api_url
        self.user_agent = user_agent
        self.consulate = consulate
        self.logger = config.get_logger()

    def _convert_to_pst(self, timestamp_string: str) -> str:
        """
        Convert GMT timestamp to PST format.
        
        Args:
            timestamp_string: GMT timestamp in format 'Wed, 07 Aug 2024 02:30:42 GMT'
            
        Returns:
            Formatted PST timestamp string
            
        Raises:
            ValueError: If timestamp format is invalid
        """
        try:
            gmt_datetime = datetime.strptime(
                timestamp_string,
                '%a, %d %b %Y %H:%M:%S GMT'
            )
            gmt_timezone = pytz.timezone('GMT')
            gmt_aware_datetime = gmt_timezone.localize(gmt_datetime)

            pst_timezone = pytz.timezone('America/Los_Angeles')
            pst_aware_datetime = gmt_aware_datetime.astimezone(pst_timezone)

            return pst_aware_datetime.strftime('%a, %d %b %Y %I:%M:%S %p')
        except ValueError as e:
            self.logger.error(f"Invalid timestamp format '{timestamp_string}': {repr(e)}")
            raise

    def _fetch_slots_data(self, access_token: str) -> Optional[list]:
        """
        Fetch visa slots data from API.
        
        Args:
            access_token: API access token
            
        Returns:
            List of slot details or None if request fails
        """
        headers = {
            'origin': config.CHROME_EXT,
            'user-agent': self.user_agent,
            'x-api-key': access_token,
            'Extversion': config.API_VERSION,
        }

        try:
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            if response.ok:
                data = response.json()
                return data.get('slotDetails')
            else:
                self.logger.warning(
                    f"API request failed with status {response.status_code}"
                )
                return None
                
        except requests.RequestException as e:
            self.logger.error(f"API request error: {repr(e)}")
            return None

    def _find_consulate_slots(
        self,
        results: list,
        consulate: Optional[str] = None
    ) -> Optional[Tuple[int, str]]:
        """
        Find slots for target consulate.
        
        Args:
            results: List of slot results
            consulate: Target consulate (uses instance default if None)
            
        Returns:
            Tuple of (slot_count, timestamp) or None if not found
        """
        target_consulate = consulate or self.consulate
        
        for result in results:
            if target_consulate in result.get("visa_location", ""):
                slot_count = result.get("slots", 0)
                timestamp = result.get("createdon", "")
                
                if timestamp:
                    timestamp = self._convert_to_pst(timestamp)
                
                return slot_count, timestamp
        
        return None

    def check_slots(self, access_token: str) -> Optional[str]:
        """
        Check for available visa slots.
        
        Args:
            access_token: API access token
            
        Returns:
            Message about available slots or None
        """
        data = self._fetch_slots_data(access_token)
        
        if not data:
            return None

        result = self._find_consulate_slots(data)
        
        if not result:
            self.logger.info(f"No slots found for consulate: {self.consulate}")
            return None

        slot_count, timestamp = result
        
        if slot_count == 0:
            return None

        message = f"Found **{slot_count}** slots at **{timestamp}**"
        self.logger.info(message)
        return message


def process_check_visa_slots(access_token: str) -> Optional[str]:
    """
    Process visa slots check (backward-compatible function).
    
    Args:
        access_token: API access token
        
    Returns:
        Message about available slots or None
    """
    checker = VisaSlotsChecker()
    return checker.check_slots(access_token)


if __name__ == '__main__':
    config.setup_logging()
    # Test with a dummy token (will fail as expected)
    result = process_check_visa_slots("TEST_TOKEN")
    print(f"Result: {result}")
