import random
import re
import hashlib
import json
import os
import logging
from telethon.tl.functions.phone import RequestCallRequest
from telethon.tl.functions.messages import GetDhConfigRequest
from telethon.tl.types import PhoneCallProtocol
from collections import defaultdict

URL = "https://cgifederal.secure.force.com/?country=India&language=English"
MESSAGE = f"An appointment is available right now! Login {URL}"

logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)


class TriggerConfig:
    def __init__(self, telegram_client, name, trigger, number=None, call=None, message=None):
        self.client = telegram_client
        self.name = name
        self.trigger = trigger
        self.number = number
        self.call = call
        self.message = message

    def __str__(self):
        return "{" + ",".join(map(str, [self.client, self.name, self.number, self.trigger, self.number, self.call, self.message])) + "}"

    async def run_trigger(self, text):
        print(f"{self.trigger}")
        if re.search(self.trigger, text):
            await self.alert()

    async def alert(self):
        if self.number is None:
            return
        if self.message:
            await self.send_message()
        if self.call:
            await self.dial_user()

    async def send_message(self):
        await self.client.send_message(self.number, f"Hello {self.name}! {MESSAGE}")

    async def dial_user(self):
        async def get_dh_config():
            class DH:
                def __init__(self, dh_config):
                    self.p = int.from_bytes(dh_config.p, 'big')
                    self.g = dh_config.g
                    self.resp = dh_config

            return DH(
                await self.client(
                    GetDhConfigRequest(version=0, random_length=256)))

        dh_config = await get_dh_config()

        def get_rand_bytes(length=256):
            return bytes(
                x ^ y for x, y in zip(os.urandom(length), dh_config.resp.random))

        def integer_to_bytes(integer):
            return int.to_bytes(
                integer,
                length=(integer.bit_length() + 8 - 1) // 8,  # 8 bits per byte,
                byteorder='big',
                signed=False
            )

        PROTOCOL = PhoneCallProtocol(
            min_layer=93,
            max_layer=93,
            udp_p2p=True,
            library_versions=['1.24.0'])
        dhc = await get_dh_config()
        a = 0
        while not (1 < a < dhc.p - 1):
            # "A chooses a random value of a, 1 < a < p-1"
            a = int.from_bytes(get_rand_bytes(), 'little')
        g_a = pow(dhc.g, a, dhc.p)

        user = await self.client.get_input_entity(self.number)
        await self.client(RequestCallRequest(
            # user_id=user.user_id,
            user_id=user,
            random_id=random.randint(0, 0x7fffffff - 1),
            g_a_hash=hashlib.sha256(integer_to_bytes(g_a)).digest(),
            protocol=PROTOCOL)
        )


async def process_triggers(text, trigger_configs):
    for trigger_config in trigger_configs:
        await trigger_config.run_trigger(text)


def load_trigger_config(telegram_client, filename, debug=False):
    try:
        with open(filename) as f:
            config = json.load(f)
            trigger_configs = list()
            print(config)
            for user in config:
                trigger_configs.append(TriggerConfig(telegram_client,
                                                     user.get('name'),
                                                     user.get('trigger'),
                                                     user.get('number'),
                                                     user.get('call'),
                                                     user.get('message')))
            logging.info("Loaded config: " +
                         "\n".join(map(str, trigger_configs)))
            return trigger_configs
    except Exception as e:
        logging.info(f"Failed to trigger configs '{filename}': {repr(e)}")
        quit()


if __name__ == '__main__':
    load_trigger_config(None, "trigger_configs.json", debug=True)
