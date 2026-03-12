import os

DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///./database.sqlite3")
HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", "8080"))
