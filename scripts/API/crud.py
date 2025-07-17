# scripts/API/crud.py

from sqlalchemy.orm import Session
from typing import List
from . import schemas

def get_top_products(db: Session, limit: int = 10) -> List[schemas.TopProduct]:
    query = """
        SELECT message AS product, COUNT(*) AS mentions
        FROM fct_messages
        WHERE message IS NOT NULL
        GROUP BY message
        ORDER BY mentions DESC
        LIMIT %(limit)s;
    """
    result = db.execute(query, {"limit": limit}).fetchall()
    return [schemas.TopProduct(product=row[0], mentions=row[1]) for row in result]

def get_top_products(db: Session, limit: int = 10):
    result = db.execute(
        """
        SELECT product_name, mentions
        FROM top_products
        ORDER BY mentions DESC
        LIMIT :limit
        """,
        {"limit": limit}
    )
    return result.fetchall()

