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
                metadata TEXT,
                priority INTEGER DEFAULT 3,
                tags TEXT
            )
        """)
        # Index for faster searches
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session ON memories(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON memories(priority)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at)")
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
    
    def add_with_priority(self, content: str, priority: int = 3, session_id: str = None, tags: str = None):
        """Add a memory with priority (1-5) and tags."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memories (content, session_id, priority, tags) VALUES (?, ?, ?, ?)",
            (content, session_id, priority, tags)
        )
        conn.commit()
        conn.close()
    
    def get_by_session(self, session_id: str) -> List[Dict]:
        """Get all memories for a specific session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at, session_id, priority, tags FROM memories WHERE session_id = ? ORDER BY created_at DESC",
            (session_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "content": r[1], "created_at": r[2], "session_id": r[3], "priority": r[4], "tags": r[5]}
            for r in rows
        ]
    
    def get_by_priority(self, min_priority: int = 3) -> List[Dict]:
        """Get memories by minimum priority."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at, session_id, priority, tags FROM memories WHERE priority >= ? ORDER BY priority DESC, created_at DESC",
            (min_priority,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "content": r[1], "created_at": r[2], "session_id": r[3], "priority": r[4], "tags": r[5]}
            for r in rows
        ]
    
    def get_stats(self) -> Dict:
        """Get statistics about stored memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM memories")
        sessions = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(priority) FROM memories WHERE priority IS NOT NULL")
        avg_priority = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_memories": total,
            "unique_sessions": sessions,
            "avg_priority": round(avg_priority, 2)
        }
    
    def export_json(self, filepath: str = None):
        """Export all memories to JSON."""
        import json
        memories = self.list_memories()
        output_path = filepath or f"{self.agent_name}_context_export.json"
        
        with open(output_path, 'w') as f:
            json.dump(memories, f, indent=2)
        
        return output_path
    
    def get_sessions(self) -> List[str]:
        """Get list of all unique session IDs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM memories WHERE session_id IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        return [r[0] for r in rows]
    
    def export_markdown(self, filepath: str = None) -> str:
        """Export all memories to Markdown file."""
        import json
        memories = self.list_memories()
        sessions = self.get_sessions()
        
        output_path = filepath or f"{self.agent_name}_context.md"
        
        with open(output_path, 'w') as f:
            f.write(f"# Agent Context: {self.agent_name}\n\n")
            f.write(f"**Exported:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Total Memories:** {len(memories)}\n\n")
            f.write(f"**Sessions:** {', '.join(sessions) if sessions else 'None'}\n\n")
            f.write("---\n\n")
            
            # Group by session
            by_session = {}
            for m in memories:
                sid = m.get('session_id', 'unknown') or 'unknown'
                if sid not in by_session:
                    by_session[sid] = []
                by_session[sid].append(m)
            
            for sid, mems in by_session.items():
                f.write(f"## Session: {sid}\n\n")
                for m in mems:
                    f.write(f"- *{m['created_at'][:16]}* - {m['content']}\n")
                f.write("\n")
        
        return output_path
    
    def get_session_summary(self, session_id: str = None) -> Dict:
        """Get a summary of memories for a session."""
        if session_id:
            memories = self.get_by_session(session_id)
        else:
            memories = self.list_memories()
        
        if not memories:
            return {"total": 0, "sessions": 0, "earliest": None, "latest": None}
        
        sessions = set(m.get('session_id') for m in memories if m.get('session_id'))
        
        return {
            "total": len(memories),
            "sessions": len(sessions),
            "earliest": memories[-1]['created_at'] if memories else None,
            "latest": memories[0]['created_at'] if memories else None
        }
    
    def get_by_tag(self, tag: str) -> List[Dict]:
        """Get memories by tag."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at, session_id, priority, tags FROM memories WHERE tags LIKE ? ORDER BY created_at DESC",
            (f"%{tag}%",)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "content": r[1], "created_at": r[2], "session_id": r[3], "priority": r[4], "tags": r[5]}
            for r in rows
        ]
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT tags FROM memories WHERE tags IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        tags = set()
        for r in rows:
            if r[0]:
                for tag in r[0].split(','):
                    tags.add(tag.strip())
        return sorted(tags)


# CLI interface
def main():
    if len(sys.argv) < 2:
        print("Usage: context-manager <command> [args]")
        print("Commands: add, list, search, clear, stats, export, sessions, tags, tag-search")
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
    
    elif cmd == "stats":
        stats = ctx.get_stats()
        print(f"Total memories: {stats['total_memories']}")
        print(f"Unique sessions: {stats['unique_sessions']}")
        print(f"Avg priority: {stats['avg_priority']}")
    
    elif cmd == "export":
        if len(sys.argv) >= 3 and sys.argv[2] == "--markdown":
            path = ctx.export_markdown()
            print(f"✓ Exported to {path}")
        else:
            path = ctx.export_json()
            print(f"✓ Exported to {path}")
    
    elif cmd == "sessions":
        sessions = ctx.get_sessions()
        if sessions:
            for s in sessions:
                print(s)
        else:
            print("No sessions found")
    
    elif cmd == "tags":
        tags = ctx.get_all_tags()
        if tags:
            print("Available tags:")
            for t in tags:
                print(f"  - {t}")
        else:
            print("No tags found")
    
    elif cmd == "tag-search":
        if len(sys.argv) < 3:
            print("Usage: context-manager tag-search <tag>")
            sys.exit(1)
        results = ctx.get_by_tag(sys.argv[2])
        print(f"Found {len(results)} memories with tag '{sys.argv[2]}':")
        for r in results:
            print(f"[{r['created_at'][:16]}] {r['content'][:80]}")
    
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: add, list, search, clear, stats, export, sessions")
        sys.exit(1)


if __name__ == "__main__":
    main()
