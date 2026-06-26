"""
Trigger system for OCR and visa slots monitoring.
"""
import re
from typing import Optional, List
from abc import ABC, abstractmethod

import config


class Trigger(ABC):
    """Abstract base class for triggers."""

    @abstractmethod
    async def check(self, data: str) -> bool:
        """
        Check if trigger condition is met.
        
        Args:
            data: Data to check against trigger
            
        Returns:
            True if trigger matches, False otherwise
        """
        pass


class RegexTrigger(Trigger):
    """Trigger based on regex pattern matching."""

    def __init__(self, pattern: str):
        """
        Initialize regex trigger.
        
        Args:
            pattern: Regex pattern to match
        """
        self.pattern = pattern

    async def check(self, text: str) -> bool:
        """
        Check if text matches regex pattern.
        
        Args:
            text: Text to check
            
        Returns:
            True if pattern matches, False otherwise
        """
        return bool(re.search(self.pattern, text))


class AlwaysTrigger(Trigger):
    """Trigger that always matches (for visa slots alerts)."""

    async def check(self, data: str) -> bool:
        """
        Always returns True if data is not empty.
        
        Args:
            data: Data to check (should be visa slot info)
            
        Returns:
            True if data is not empty
        """
        return data is not None and data != ""


class TriggerConfig:
    """Configuration for a single trigger action."""

    def __init__(
        self,
        name: str,
        trigger: Trigger,
        user_number: Optional[str] = None,
        enable_message: bool = False,
        enable_call: bool = False,
        enable_visa_slots: bool = False,
    ):
        """
        Initialize trigger configuration.
        
        Args:
            name: User/trigger name
            trigger: Trigger instance to check
            user_number: Target user phone/ID (optional)
            enable_message: Send message alerts
            enable_call: Send call alerts
            enable_visa_slots: Monitor visa slots
        """
        self.name = name
        self.trigger = trigger
        self.user_number = user_number
        self.enable_message = enable_message
        self.enable_call = enable_call
        self.enable_visa_slots = enable_visa_slots

    def __str__(self) -> str:
        return (
            f"{self.name}: number={self.user_number}, trigger={self.trigger.__class__.__name__}, "
            f"message={self.enable_message}, call={self.enable_call}, "
            f"visa_slots={self.enable_visa_slots}"
        )


class TriggerManager:
    """Manages trigger execution and alerts."""

    def __init__(self, telegram_client, message_handler, call_handler):
        """
        Initialize trigger manager.
        
        Args:
            telegram_client: Telethon TelegramClient instance
            message_handler: Alert handler for messages
            call_handler: Phone call handler
        """
        self.client = telegram_client
        self.message_handler = message_handler
        self.call_handler = call_handler

    async def process_ocr_triggers(
        self,
        text: str,
        photo_path: str,
        message,
        trigger_configs: List[TriggerConfig]
    ) -> None:
        """
        Process OCR triggers for detected text.
        
        Args:
            text: OCR-extracted text
            photo_path: Path to processed image
            message: Original Telegram message object
            trigger_configs: List of trigger configurations to check
        """
        logger = config.get_logger()
        
        for config_item in trigger_configs:
            if not config_item.user_number:
                continue

            try:
                if await config_item.trigger.check(text):
                    logger.info(f"OCR trigger matched for {config_item.name}")

                    if config_item.enable_message:
                        message_sent = await self.message_handler.send_alert(
                            config_item.user_number,
                            f"Hello {config_item.name}!",
                            config.VISA_ALERT_MESSAGE,
                            photo_path
                        )
                        if not message_sent:
                            logger.error(
                                f"Failed to send OCR alert message to {config_item.user_number} "
                                f"for {config_item.name}. See handler logs for details."
                            )

                    if config_item.enable_call:
                        call_placed = await self.call_handler.call_user(config_item.user_number)
                        if not call_placed:
                            logger.error(
                                f"Failed to place OCR alert call to {config_item.user_number} "
                                f"for {config_item.name}. See handler logs for details."
                            )
            except Exception as e:
                logger.warning(f"Error processing OCR trigger for {config_item.name}: {repr(e)}")

    async def process_visa_slots_triggers(
        self,
        slots_message: Optional[str],
        trigger_configs: List[TriggerConfig]
    ) -> None:
        """
        Process visa slots triggers.
        
        Args:
            slots_message: Message about available slots (or None)
            trigger_configs: List of trigger configurations to check
        """
        logger = config.get_logger()

        if slots_message is None or slots_message == "":
            return

        for config_item in trigger_configs:
            if not config_item.user_number or not config_item.enable_visa_slots:
                continue

            try:
                if await config_item.trigger.check(slots_message):
                    logger.info(f"Visa slots trigger matched for {config_item.name}")

                    message = f"Hello {config_item.name}! {config.VISA_ALERT_MESSAGE}\nSource checkvisaslots.com:\n{slots_message}"
                    message_sent = await self.message_handler.send_alert(
                        config_item.user_number,
                        "",
                        message
                    )
                    if not message_sent:
                        logger.error(
                            f"Failed to send visa slots alert message to {config_item.user_number} "
                            f"for {config_item.name}. See handler logs for details."
                        )
            except Exception as e:
                logger.warning(f"Error processing visa slots trigger for {config_item.name}: {repr(e)}")
