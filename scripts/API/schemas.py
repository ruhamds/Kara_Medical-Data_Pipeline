from pydantic import BaseModel
from typing import List

class TopProduct(BaseModel):
    product: str
    mentions: int
    class Config:
        from_attributes = True

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int

class PostingTrend(BaseModel):
    date: str
    message_count: int

class TelegramMessage(BaseModel):
    id: int
    text: str
    date: str
    channel_name: str

    class Config:
        orm_mode = True

class TopDetectedObject(BaseModel):
    object_label: str
    count: int

    class Config:
        orm_mode = True