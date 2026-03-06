"""
Agent Context Manager - Lightweight context management for AI agents.
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DB_FILE = "context.db"

class ContextManager:
    """Lightweight context manager with SQLite backend."""
    
    def __init__(self, agent_name: str = "default", db_path: str = None):
        self.agent_name = agent_name
        self.db_path = db_path or f"{agent_name}_{DB_FILE}"
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                metadata TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def add(self, content: str, session_id: str = None, metadata: str = None):
        """Add a memory to context."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memories (content, session_id, metadata) VALUES (?, ?, ?)",
            (content, session_id, metadata)
        )
        conn.commit()
        conn.close()
    
    def get_context(self, max_tokens: int = 2000) -> str:
        """Get all memories as context string."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content, created_at FROM memories ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # Simple token estimation (rough: 4 chars per token)
        context_parts = []
        current_tokens = 0
        
        for content, created_at in rows:
            content_tokens = len(content) // 4
            if current_tokens + content_tokens > max_tokens:
                break
            context_parts.append(f"[{created_at[:16]}] {content}")
            current_tokens += content_tokens
        
        return "\n".join(reversed(context_parts))
    
    def list_memories(self) -> List[Dict]:
        """List all memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, created_at, session_id FROM memories ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "content": r[1], "created_at": r[2], "session_id": r[3]}
            for r in rows
        ]
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Simple substring search."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at, session_id FROM memories WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "content": r[1], "created_at": r[2], "session_id": r[3]}
            for r in rows
        ]
    
    def clear_older_than(self, days: int = 30):
        """Clear memories older than specified days."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute("DELETE FROM memories WHERE created_at < ?", (cutoff,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted
    
    def clear_all(self):
        """Clear all memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories")
        conn.commit()
        conn.close()


# CLI interface
def main():
    if len(sys.argv) < 2:
        print("Usage: context-manager <command> [args]")
        print("Commands: add, list, search, clear")
        sys.exit(1)
    
    cmd = sys.argv[1]
    ctx = ContextManager()
    
    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: context-manager add <content>")
            sys.exit(1)
        ctx.add(" ".join(sys.argv[2:]))
        print("✓ Memory added")
    
    elif cmd == "list":
        memories = ctx.list_memories()
        for m in memories:
            print(f"[{m['created_at'][:16]}] {m['content']}")
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: context-manager search <query>")
            sys.exit(1)
        results = ctx.search(sys.argv[2])
        for r in results:
            print(f"[{r['created_at'][:16]}] {r['content']}")
    
    elif cmd == "clear":
        days = 30
        if len(sys.argv) > 2 and sys.argv[2] == "--days":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        deleted = ctx.clear_older_than(days)
        print(f"✓ Cleared {deleted} memories older than {days} days")
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
