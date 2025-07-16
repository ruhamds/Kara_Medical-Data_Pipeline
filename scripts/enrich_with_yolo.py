import os
import psycopg2
import json
from ultralytics import YOLO
from dotenv import load_dotenv
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(filename='logs/enrich_images.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load env variables
load_dotenv()
DB_HOST = 'localhost'
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_PORT = os.getenv('POSTGRES_PORT')

# Load YOLO model
model = YOLO('yolov8n.pt')

def create_detected_objects_table():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.detected_objects (
            message_id BIGINT,
            object_label VARCHAR(100),
            confidence FLOAT,
            bounding_box JSONB,
            media_path TEXT,
            PRIMARY KEY (message_id, object_label)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("✅ Created detected_objects table")

def enrich_images():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, media_path 
        FROM raw.telegram_messages 
        WHERE has_media = TRUE 
        AND media_type = 'MessageMediaPhoto' 
        AND media_path LIKE '%jpg'
        LIMIT 100;
    """)
    images = cursor.fetchall()
    
    for message_id, media_path in images:
        try:
            if not Path(media_path).exists():
                logging.warning(f"❌ Image not found: {media_path}")
                continue

            print(f"📸 Processing image {message_id}: {media_path}")
            results = model(media_path)

            for result in results:
                for box in result.boxes:
                    label = model.names[int(box.cls)]
                    confidence = float(box.conf)
                    bbox = {
                        "x": float(box.xywh[0][0]),
                        "y": float(box.xywh[0][1]),
                        "width": float(box.xywh[0][2]),
                        "height": float(box.xywh[0][3])
                    }

                    print(f"✅ Inserting: {message_id}, {label}, {confidence:.2f}, {bbox}")

                    try:
                        cursor.execute("""
                            INSERT INTO public.detected_objects (message_id, object_label, confidence, bounding_box, media_path)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
                        """, (message_id, label, confidence, json.dumps(bbox), media_path))
                        print("✅ Inserted into DB")

                    except Exception as e:
                        print(f"❌ Failed to insert: {e}")
                        logging.error(f"❌ DB Insert error: {e}")
                        conn.rollback()

            conn.commit()
            logging.info(f"✅ Processed image for message_id {message_id}")

        except Exception as e:
            logging.error(f"❌ Error processing image {media_path}: {str(e)}")
            conn.rollback()

    cursor.close()
    conn.close()
    logging.info(f"🏁 Finished processing {len(images)} images")

if __name__ == "__main__":
    create_detected_objects_table()
    enrich_images()
