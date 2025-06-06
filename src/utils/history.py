import sqlite3
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class History:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(History, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # init db with the table
        self.db_path = Path(__file__).parent.parent / 'user' / 'history.db'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS "history" (
                    "id" INTEGER NOT NULL UNIQUE,
                    "title" TEXT NOT NULL,
                    "url" TEXT NOT NULL,
                    "timestamp" TIMESTAMP NOT NULL,
                    PRIMARY KEY("id")
                )
            """)
            
            # allows us to search faster by time
            conn.execute("""
                CREATE INDEX IF NOT EXISTS "idx_timestamp" ON "history" ("timestamp" DESC)
            """)
    
    def _get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
    
    def add_entry(self, title: str, url: str):
        # add history entry
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO history (title, url, timestamp) VALUES (?, ?, ?)",
                (title, url, datetime.now().isoformat())
            )
    
    def get_entries(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        # get all of the users history with pages
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM history ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def search(self, query: str, limit: int = 100) -> List[Dict]:
        # search by title or url
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM history 
                WHERE title LIKE ? OR url LIKE ? 
                ORDER BY timestamp DESC 
                LIMIT ?
                """,
                (f"%{query}%", f"%{query}%", limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_entry(self, entry_id: int):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    
    def clear_history(self):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM history")
            
    def get_entry_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM history")
            return cursor.fetchone()[0]

history = History()