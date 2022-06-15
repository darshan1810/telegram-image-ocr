from concurrent.futures import process
from telethon import TelegramClient, events
from process_image import process_image
from process_triggers import process_triggers, load_trigger_config
import json
import logging
import asyncio

IMG_DIR="./img/"

logging.basicConfig(
    filename="logs.log",
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO
)


async def work(client, trigger_config_filename):
    trigger_config = load_trigger_config(client, trigger_config_filename)
    async with client:
        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            message = event.message
            if message.photo:
                photo = await message.download_media(file=IMG_DIR)
                text = process_image(photo)
                logging.info(text)
                await process_triggers(text, photo, trigger_config)
            logging.info(message.message)
        await client.run_until_disconnected()


async def main():
    # Load api credentials from the session config.
    try:
        with open("session.conf") as f:
            conf = json.load(f)
            api_id = conf.get('api_id')
            api_hash = conf.get('api_hash')
            session_name = conf.get('session_name')
            trigger_config_filename = conf.get('trigger_config_filename')
    except Exception as e:
        logging.info(f"Failed to load session.conf: {repr(e)}")
        quit()
    await work(TelegramClient(session_name, api_id, api_hash), trigger_config_filename)


asyncio.run(main())
