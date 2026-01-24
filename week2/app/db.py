from __future__ import annotations

import sqlite3
from pathlib import Path 
from typing import Optional
from contextlib import contextmanager

# BASE_DIR = Path(__file__).resolve().parents[1]
# DATA_DIR = BASE_DIR / "data"
# DB_PATH = DATA_DIR / "app.db"

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_data_directory_exists()
        self.init_db()

    def _ensure_data_directory_exists(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection(self) -> ContextManager[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                );
                """
            )
            conn.commit()

    def insert_note(self, content: str) -> int:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            conn.commit()
            return int(cursor.lastrowid)

    def list_notes(self) -> list[sqlite3.Row]:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            return list(cursor.fetchall())

    def get_note(self, note_id: int) -> Optional[sqlite3.Row]:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            return cursor.fetchone()
    def get_action_item(self, item_id: int) -> Optional[sqlite3.Row]:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items WHERE id = ?",
                (item_id,),
            )
            return cursor.fetchone()
    def insert_action_item(self, note_id: int, text: str) -> int:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                (note_id, text),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def insert_action_items(self, items: list[str], note_id: Optional[int] = None) -> list[int]:
        """批量插入行动项"""
        with self.connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []

            # 使用executemany进行批量插入，比循环单条插入更高效
            if note_id is None:
                data = [(item,) for item in items]
                cursor.executemany("INSERT INTO action_items (text) VALUES (?)", data)
            else:
                data = [(note_id, item) for item in items]
                cursor.executemany("INSERT INTO action_items (note_id, text) VALUES (?, ?)", data)

            connection.commit()

            # 获取插入的ID范围
            last_id = cursor.lastrowid
            
            # 处理cursor.lastrowid为None的情况（SQLite版本<3.37.0时executemany会返回None）
            if last_id is None:
                # 使用另一种方式获取最后插入的ID
                cursor.execute("SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]
            
            return list(range(last_id - len(items) + 1, last_id + 1))
            
    def list_action_items(self, note_id: Optional[int] = None) -> list[sqlite3.Row]:
        with self.connection() as conn:
            cursor = conn.cursor()
            if note_id is None:
                cursor.execute("SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC")
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            return list(cursor.fetchall())
            
    def mark_action_item_done(self, item_id: int, done: bool = True) -> None:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (done, item_id),
            )
            conn.commit()


# 初始化全局数据库实例
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"
db = Database(DB_PATH)



