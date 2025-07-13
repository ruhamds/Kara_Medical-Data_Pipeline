import os
import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
import asyncio

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')


# Data lake path
DATA_LAKE_PATH = Path('data/raw/telegram_messages')
LOG_PATH = Path('logs/scrape_telegram.log')

# Channel list
CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/tikvahpharma',
    'https://t.me/ChemedPharma'
]

# Create folders
DATA_LAKE_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sanitize_channel_name(url):
    return urlparse(url).path.strip('/')

async def scrape_channel(client, channel_url, date):
    try:
        channel_name = sanitize_channel_name(channel_url)
        logger.info(f"Scraping {channel_name} for {date}")

        entity = await client.get_entity(channel_url)
        messages = []

        async for message in client.iter_messages(entity, limit=5000, offset_date=date):
            if not message.message and not message.media:
                continue

            msg_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.message or '',
                'has_media': bool(message.media),
                'media_type': type(message.media).__name__ if message.media else None,
                'channel': channel_name
            }

            if message.media and hasattr(message.media, 'photo'):
                media_path = DATA_LAKE_PATH / date.strftime('%Y-%m-%d') / channel_name / f"media_{message.id}.jpg"
                media_path.parent.mkdir(parents=True, exist_ok=True)
                await client.download_media(message.media, media_path)
                msg_data['media_path'] = str(media_path)
                logger.info(f"Downloaded media for message {message.id} to {media_path}")

            messages.append(msg_data)

        if messages:
            json_path = DATA_LAKE_PATH / date.strftime('%Y-%m-%d') / channel_name / 'messages.json'
            json_path.parent.mkdir(parents=True, exist_ok=True)
            with json_path.open('w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(messages)} messages to {json_path}")
        else:
            logger.warning(f"No messages found for {channel_name} on {date}")

    except FloodWaitError as e:
        logger.warning(f"Rate limit hit. Sleeping for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.error(f"Error scraping {channel_url}: {str(e)}")

async def main():
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        if not await client.is_user_authorized():
            await client.send_code_request(PHONE)
            code = input("Enter the code you received: ")
            try:
                await client.sign_in(PHONE, code)
            except SessionPasswordNeededError:
                password = input("Enter your 2FA password: ")
                await client.sign_in(password=password)

        today = datetime.now().date()
        for channel_url in CHANNELS:
            await scrape_channel(client, channel_url, today)

if __name__ == '__main__':
    asyncio.run(main())
