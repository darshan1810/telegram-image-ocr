"""
Phone call handling module using Telegram's peer-to-peer calling protocol.
"""
import hashlib
import os
import random
from typing import Optional

from telethon.tl.functions.phone import RequestCallRequest
from telethon.tl.functions.messages import GetDhConfigRequest
from telethon.tl.types import PhoneCallProtocol

import config


class PhoneCallHandler:
    """Handles peer-to-peer phone calls via Telegram."""

    def __init__(self, telegram_client):
        """
        Initialize phone call handler.
        
        Args:
            telegram_client: Telethon TelegramClient instance
        """
        self.client = telegram_client

    async def _get_dh_config(self):
        """
        Retrieve Diffie-Hellman configuration from Telegram.
        
        Returns:
            DH config object with p, g, and random parameters
        """
        class DHConfig:
            def __init__(self, dh_config):
                self.p = int.from_bytes(dh_config.p, 'big')
                self.g = dh_config.g
                self.resp = dh_config

        dh_resp = await self.client(GetDhConfigRequest(version=0, random_length=256))
        return DHConfig(dh_resp)

    def _get_random_bytes(self, dh_config, length: int = 256) -> bytes:
        """
        Generate random bytes XORed with Telegram's random.
        
        Args:
            dh_config: DH config containing random bytes
            length: Number of random bytes to generate
            
        Returns:
            Random bytes
        """
        return bytes(
            x ^ y for x, y in zip(os.urandom(length), dh_config.resp.random)
        )

    @staticmethod
    def _integer_to_bytes(integer: int) -> bytes:
        """
        Convert integer to bytes.
        
        Args:
            integer: Integer to convert
            
        Returns:
            Bytes representation of integer
        """
        return int.to_bytes(
            integer,
            length=(integer.bit_length() + 8 - 1) // 8,
            byteorder='big',
            signed=False
        )

    async def call_user(self, user_number: str) -> bool:
        """
        Initiate a phone call to a user.
        
        Args:
            user_number: Telegram phone number or user ID
            
        Returns:
            True if call initiated successfully, False otherwise
        """
        try:
            dh_config = await self._get_dh_config()

            # Generate random 'a' value: 1 < a < p-1
            a = 0
            while not (1 < a < dh_config.p - 1):
                a = int.from_bytes(self._get_random_bytes(dh_config), 'little')

            # Calculate g^a mod p
            g_a = pow(dh_config.g, a, dh_config.p)

            # Get user entity
            user = await self.client.get_input_entity(user_number)

            # Create phone call protocol
            protocol = PhoneCallProtocol(
                min_layer=config.PHONE_CALL_PROTOCOL_VERSION,
                max_layer=config.PHONE_CALL_PROTOCOL_VERSION,
                udp_p2p=True,
                library_versions=[config.PHONE_CALL_LIBRARY_VERSION]
            )

            # Request call
            await self.client(
                RequestCallRequest(
                    user_id=user,
                    random_id=random.randint(0, 0x7fffffff - 1),
                    g_a_hash=hashlib.sha256(self._integer_to_bytes(g_a)).digest(),
                    protocol=protocol
                )
            )
            return True
        except Exception as e:
            config.get_logger().warning(f"Failed to initiate phone call: {repr(e)}")
            return False
