"""
Centralized configuration and constants module.
"""
import logging
import os
from typing import Optional

# Image processing
IMG_DIR = "./img/"

# Telegram session defaults
DEFAULT_SESSION_CONFIG_FILE = "session.conf"
DEFAULT_TRIGGER_CONFIG_FILE = "trigger_configs.json"

# Visa slots checking
SLOTS_URL = "https://app.checkvisaslots.com/slots/v3"
CHROME_EXT = "chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
API_VERSION = "4.5.5"
DEFAULT_CONSULATE = "CHENNAI"

# Alert messages
VISA_APPOINTMENT_URL = "https://www.usvisascheduling.com/en-US/"
VISA_ALERT_MESSAGE = f"An appointment maybe available right now! Login {VISA_APPOINTMENT_URL}"

# Visa slots check timing (in seconds)
MIN_CVS_SLEEP = 600  # 10 minutes
MAX_CVS_SLEEP = 3601  # ~1 hour

# Phone call setup
PHONE_CALL_PROTOCOL_VERSION = 93
PHONE_CALL_LIBRARY_VERSION = "1.24.0"

# Telegram monitor setup delay
TELEGRAM_STARTUP_DELAY = 10

# Logging configuration
LOG_FILE = "logs.log"
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(message)s'
LOG_LEVEL = logging.INFO


def setup_logging(
    log_file: str = LOG_FILE,
    log_format: str = LOG_FORMAT,
    level: int = LOG_LEVEL,
) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_file: Path to log file
        log_format: Log message format
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format=log_format,
        level=level,
    )
    return logging.getLogger(__name__)


def get_logger() -> logging.Logger:
    """Get configured logger instance."""
    return logging.getLogger(__name__)
