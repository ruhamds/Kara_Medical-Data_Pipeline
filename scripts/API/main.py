from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from .database import SessionLocal, engine

# Create tables if not already created
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kara Medical Data Analytical API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = Query(10, description="Limit number of products"), db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit=limit)

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name=channel_name)

@app.get("/api/search/messages", response_model=List[schemas.TelegramMessage])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query=query)

@app.get("/api/reports/top-detections", response_model=List[schemas.TopDetectedObject])
def top_detected_objects(limit: int = Query(10), db: Session = Depends(get_db)):
    return crud.get_top_detected_objects(db, limit=limit)

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def read_top_products(limit: int = 10, db: Session = Depends(get_db)):
    print(f"📦 Request received: limit={limit}")
    return get_top_products(db, limit)
