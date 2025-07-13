import os
import json
import logging
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# Setup logging
Path('logs').mkdir(exist_ok=True)
logging.basicConfig(
    filename='logs/load_to_postgres.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database config
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'telegram_db'),
    'user': os.getenv('POSTGRES_USER', 'user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),  # use 'db' in Docker
    'port': os.getenv('POSTGRES_PORT', '5432')
}

# Data path
DATA_LAKE_PATH = Path('data/raw/telegram_messages')

def create_raw_table(conn):
    """Create schema and telegram_messages table."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                    id BIGINT PRIMARY KEY,
                    date TIMESTAMP,
                    text TEXT,
                    has_media BOOLEAN,
                    media_type VARCHAR(50),
                    channel VARCHAR(100),
                    media_path TEXT
                );
            """)
        conn.commit()
        logger.info("Schema and table created successfully.")
    except Exception:
        logger.exception("Failed to create schema or table.")
        conn.rollback()
        raise

def load_json_to_postgres(json_path, conn):
    """Load one JSON file into PostgreSQL."""
    try:
        with json_path.open('r', encoding='utf-8') as f:
            messages = json.load(f)

        rows = []
        for msg in messages:
            try:
                rows.append((
                    msg['id'],
                    msg['date'],
                    msg['text'],
                    msg['has_media'],
                    msg['media_type'],
                    msg['channel'],
                    msg.get('media_path')
                ))
            except KeyError as e:
                logger.warning(f"Missing key {e} in message {msg.get('id')}, skipping.")

        with conn.cursor() as cur:
            execute_batch(cur, """
                INSERT INTO raw.telegram_messages (id, date, text, has_media, media_type, channel, media_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, rows, page_size=1000)

        conn.commit()
        logger.info(f"Loaded {len(rows)} messages from {json_path}")
        return len(rows)

    except Exception:
        logger.exception(f"Error processing {json_path}")
        conn.rollback()
        return 0

def main():
    """Load all message JSONs into the raw schema."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        create_raw_table(conn)

        total = 0
        for json_file in DATA_LAKE_PATH.glob('2025-07-12/*/messages.json'):
            total += load_json_to_postgres(json_file, conn)

        logger.info(f"Total loaded: {total}")
        print(f"✅ Loaded {total} messages into raw.telegram_messages")

    except Exception:
        logger.exception("Failed to load messages")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
