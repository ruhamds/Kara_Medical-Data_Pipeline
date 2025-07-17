from sqlalchemy import Column, Integer, String, Text, Float, Date, BigInteger, JSON
from .database import Base

class StgTelegramMessages(Base):
    __tablename__ = "stg_telegram_messages"

    id = Column(BigInteger, primary_key=True, index=True)
    date = Column(Date)
    channel_name = Column(String)
    message_text = Column(Text)
    media_type = Column(String)
    has_media = Column(String)

class StgDetectedObjects(Base):
    __tablename__ = "stg_detected_objects"

    message_id = Column(BigInteger, primary_key=True, index=True)
    object_label = Column(String, primary_key=True)
    confidence = Column(Float)
    bounding_box = Column(JSON)
    media_path = Column(Text)

class TopDetectedObjects(Base):
    __tablename__ = "top_detected_objects"

    object_label = Column(String, primary_key=True)
    total_detections = Column(Integer)
