"""
Alert handlers for different notification channels.
"""
from abc import ABC, abstractmethod
from typing import Optional

import config


class AlertHandler(ABC):
    """Abstract base class for alert handlers."""

    @abstractmethod
    async def send_alert(self, recipient: str, title: str, message: str, photo_path: Optional[str] = None) -> bool:
        """
        Send an alert notification.
        
        Args:
            recipient: Target recipient (phone number, user ID, etc.)
            title: Alert title
            message: Alert message
            photo_path: Optional path to photo to attach
            
        Returns:
            True if alert sent successfully, False otherwise
        """
        pass


class TelegramMessageHandler(AlertHandler):
    """Sends alerts via Telegram messages."""

    def __init__(self, telegram_client):
        """
        Initialize Telegram message handler.
        
        Args:
            telegram_client: Telethon TelegramClient instance
        """
        self.client = telegram_client

    async def send_alert(
        self,
        recipient: str,
        title: str,
        message: str,
        photo_path: Optional[str] = None
    ) -> bool:
        """
        Send alert via Telegram message.
        
        Args:
            recipient: Target user number
            title: Alert title
            message: Alert message
            photo_path: Optional photo to attach
            
        Returns:
            True if successful, False otherwise
        """
        try:
            full_message = f"{title}\n{message}"
            await self.client.send_message(recipient, full_message, parse_mode='md')

            if photo_path:
                try:
                    await self.client.send_file(recipient, photo_path, caption="Attached image:", force_document=False)
                except Exception as e:
                    config.get_logger().warning(f"Failed to send photo: {repr(e)}")

            return True
        except Exception as e:
            config.get_logger().warning(f"Failed to send Telegram message: {repr(e)}")
            return False


class TelegramForwardHandler(AlertHandler):
    """Forwards original message via Telegram."""

    def __init__(self, telegram_client):
        """
        Initialize Telegram forward handler.
        
        Args:
            telegram_client: Telethon TelegramClient instance
        """
        self.client = telegram_client

    async def send_alert(
        self,
        recipient: str,
        title: str,
        message,  # Can be Telegram message object
        photo_path: Optional[str] = None
    ) -> bool:
        """
        Forward original Telegram message to recipient.
        
        Args:
            recipient: Target user number
            title: Alert title
            message: Original Telegram message object to forward
            photo_path: Fallback photo if forward fails
            
        Returns:
            True if successful, False otherwise
        """
        try:
            await self.client.send_message(recipient, title, parse_mode='md')
            await self.client.forward_messages(recipient, message)
            return True
        except Exception as e:
            config.get_logger().warning(f"Forwarding failed: {repr(e)}")
            
            # Fallback to sending photo if provided
            if photo_path:
                try:
                    await self.client.send_file(recipient, photo_path, caption="Attached image:", force_document=False)
                    return True
                except Exception as fallback_e:
                    config.get_logger().warning(f"Fallback also failed: {repr(fallback_e)}")
            
            return False
