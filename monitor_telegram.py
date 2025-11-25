"""
Main Telegram monitoring application.
Listens for images and visa slot availability updates.
"""
import asyncio
import json
import logging
import random
from typing import List, Optional

from telethon import TelegramClient, events

# Import new modular components
import config
from trigger_config_loader import load_trigger_config
from process_image import process_image
from process_check_visa_slots import process_check_visa_slots, VisaSlotsChecker
from phone_call import PhoneCallHandler
from alert_handlers import TelegramMessageHandler
from triggers import TriggerManager


class TelegramMonitor:
    """Main Telegram monitoring orchestrator."""

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_name: str,
        access_tokens: List[str],
        trigger_config_file: str,
    ):
        """
        Initialize Telegram monitor.
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API hash
            session_name: Session file name
            access_tokens: List of visa slots API tokens
            trigger_config_file: Path to trigger config JSON
        """
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.access_tokens = access_tokens
        self.trigger_config_file = trigger_config_file
        self.trigger_configs = None
        self.trigger_manager = None
        self.visa_checker = VisaSlotsChecker()
        self.logger = config.get_logger()

    async def _initialize(self) -> bool:
        """
        Initialize monitor and load configurations.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Load trigger configurations
            self.trigger_configs = load_trigger_config(
                self.client,
                self.trigger_config_file
            )

            # Initialize handlers
            message_handler = TelegramMessageHandler(self.client)
            call_handler = PhoneCallHandler(self.client)

            # Initialize trigger manager
            self.trigger_manager = TriggerManager(
                self.client,
                message_handler,
                call_handler
            )

            return True
        except Exception as e:
            self.logger.error(f"Initialization failed: {repr(e)}")
            return False

    async def monitor_images(self) -> None:
        """Listen for and process incoming images."""
        @self.client.on(events.NewMessage(incoming=True))
        async def image_handler(event):
            try:
                message = event.message

                # Process images
                if message.photo:
                    photo_path = await message.download_media(
                        file=config.IMG_DIR
                    )
                    
                    try:
                        text = process_image(photo_path)
                        self.logger.info(f"OCR result: {text}")
                        
                        if self.trigger_manager:
                            await self.trigger_manager.process_ocr_triggers(
                                text,
                                photo_path,
                                message,
                                self.trigger_configs
                            )
                    except Exception as e:
                        self.logger.warning(f"Image processing error: {repr(e)}")

                # Log all messages for debugging
                if message.message:
                    self.logger.debug(f"Message: {message.message}")

            except Exception as e:
                self.logger.warning(f"Message handler error: {repr(e)}")

        await self.client.run_until_disconnected()

    async def monitor_visa_slots(self) -> None:
        """Periodically check for available visa slots."""
        # Wait for client to connect
        await asyncio.sleep(config.TELEGRAM_STARTUP_DELAY)

        token_index = 0
        
        while True:
            try:
                # Rotate through access tokens
                token_index = (token_index + 1) % len(self.access_tokens)
                access_token = self.access_tokens[token_index]

                # Check for available slots
                slots_message = process_check_visa_slots(access_token)

                # Process triggers if slots found
                if slots_message and self.trigger_manager:
                    await self.trigger_manager.process_visa_slots_triggers(
                        slots_message,
                        self.trigger_configs
                    )

                # Sleep before next check
                sleep_duration = random.randint(
                    config.MIN_CVS_SLEEP,
                    config.MAX_CVS_SLEEP
                )
                self.logger.info(f"Next visa slots check in {sleep_duration}s")
                await asyncio.sleep(sleep_duration)

            except Exception as e:
                self.logger.warning(f"Visa slots check error: {repr(e)}")
                await asyncio.sleep(config.MIN_CVS_SLEEP)

    async def run(self) -> None:
        """Start the Telegram monitor."""
        try:
            # Initialize
            if not await self._initialize():
                return

            # Connect and run
            async with self.client:
                # Start background visa slots monitoring
                visa_monitor_task = asyncio.create_task(self.monitor_visa_slots())

                try:
                    # Run main image monitoring loop
                    await self.monitor_images()
                finally:
                    visa_monitor_task.cancel()

        except Exception as e:
            self.logger.error(f"Monitor error: {repr(e)}")
            raise


async def main():
    """Main entry point."""
    logger = config.setup_logging()

    try:
        # Load configuration
        with open(config.DEFAULT_SESSION_CONFIG_FILE) as f:
            conf = json.load(f)
            api_id = conf.get('api_id')
            api_hash = conf.get('api_hash')
            session_name = conf.get('session_name')
            trigger_config_filename = conf.get(
                'trigger_config_filename',
                config.DEFAULT_TRIGGER_CONFIG_FILE
            )
            access_tokens = conf.get('access_tokens', [])

            if not all([api_id, api_hash, session_name, access_tokens]):
                raise ValueError("Missing required configuration fields")

    except FileNotFoundError:
        logger.error(
            f"Config file not found: {config.DEFAULT_SESSION_CONFIG_FILE}. "
            f"Please create it from sample_session.conf"
        )
        return
    except Exception as e:
        logger.error(f"Failed to load configuration: {repr(e)}")
        return

    # Create and run monitor
    monitor = TelegramMonitor(
        api_id,
        api_hash,
        session_name,
        access_tokens,
        trigger_config_filename
    )

    await monitor.run()


if __name__ == "__main__":
    asyncio.run(main())
