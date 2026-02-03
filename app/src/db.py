import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def wait_for_db(max_attempts: int = 20, sleep_seconds: int = 2) -> None:
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            conn = get_conn()
            conn.close()
            return
        except Exception as e:
            last_err = e
            print(f"[db] not ready (attempt {attempt}/{max_attempts}): {e}")
            time.sleep(sleep_seconds)
    raise RuntimeError(f"Database never became ready: {last_err}")

def init_db():
    """Creates a simple table if it doesn't exist."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    visited_at TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()
    finally:
        conn.close()

def record_visit():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO visits DEFAULT VALUES RETURNING id, visited_at;")
            row = cur.fetchone()
        conn.commit()
        return row
    finally:
        conn.close()

def count_visits() -> int:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM visits;")
            row = cur.fetchone()
        return int(row["count"])
    finally:
        conn.close()
