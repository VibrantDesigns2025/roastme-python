import sqlite3, os

# where to persist your usage data
DB_PATH = os.getenv("USAGE_DB", "usage.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      count INTEGER NOT NULL DEFAULT 0,
      is_premium INTEGER NOT NULL DEFAULT 0
    )
    """)
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Initialized DB at", DB_PATH)
