from sqlalchemy import create_engine, text
from shared.config import DB_URL

engine = create_engine(DB_URL)

def insert_object(x, y, depth):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO detected_objects (x, y, depth) VALUES (:x, :y, :depth)
        """), {"x": x, "y": y, "depth": depth})