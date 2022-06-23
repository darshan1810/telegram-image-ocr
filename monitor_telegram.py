from concurrent.futures import process
from telethon import TelegramClient, events
from process_check_visa_slots import process_check_visa_slots
from process_image import process_image
from process_triggers import process_check_visa_slot_triggers, process_ocr_triggers, load_trigger_config
import asyncio
import json
import logging
import random

IMG_DIR = "./img/"

logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)


async def telegram_monitor(client, trigger_config):
    async with client:
        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            message = event.message
            if message.photo:
                photo = await message.download_media(file=IMG_DIR)
                text = process_image(photo)
                logging.info(text)
                await process_ocr_triggers(text, photo, trigger_config)
            logging.info(message.message)
        await client.run_until_disconnected()


async def check_visa_slots_monitor(access_tokens, trigger_config):
    # Need a setup sleep to wait for telegram client connection
    await asyncio.sleep(10)
    i = 0
    while True:
        i = (i + 1) % len(access_tokens)
        response = process_check_visa_slots(access_tokens[i])
        await process_check_visa_slot_triggers(response, trigger_config)
        retry_sleep_secs = random.randint(600, 3601)
        logging.info(f"CVS: Going to sleep for {retry_sleep_secs}s")
        await asyncio.sleep(retry_sleep_secs)


async def main():
    # Load api credentials from the session config.
    try:
        with open("session.conf") as f:
            conf = json.load(f)
            api_id = conf.get('api_id')
            api_hash = conf.get('api_hash')
            session_name = conf.get('session_name')
            trigger_config_filename = conf.get('trigger_config_filename')
            access_tokens = conf.get('access_tokens')
    except Exception as e:
        logging.info(f"Failed to load session.conf: {repr(e)}")
        quit()
    telegram_client = TelegramClient(session_name, api_id, api_hash)
    trigger_config = load_trigger_config(
        telegram_client, trigger_config_filename)
    bg_task = asyncio.create_task(
        check_visa_slots_monitor(access_tokens, trigger_config))
    await telegram_monitor(telegram_client, trigger_config)


asyncio.run(main())
