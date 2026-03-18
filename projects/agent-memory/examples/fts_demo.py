#!/usr/bin/env python3
"""
Agent Memory - SQLite-backed with Full-Text Search
==================================================
Use SQLite FTS5 for better search.

Usage:
    memory = Memory(storage="fts", path="./memory.db")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


# Note: This requires pysqlite3 or Python 3.11+ with FTS5 support
# For demo, we'll use the SQLite backend

def demo_fts():
    """Demo full-text search features."""
    import tempfile
    demo_path = os.path.join(tempfile.gettempdir(), "fts_demo.db")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - SQLite Full-Text Search Demo")
    print("=" * 50)
    
    # Use SQLite backend
    memory = Memory(storage="sqlite", path=demo_path, ttl_days=30)
    
    # Add memories with different content
    print("\n1. Adding memories...")
    memory.add("Python is a great programming language", metadata={"topic": "python"})
    memory.add("JavaScript is used for web development", metadata={"topic": "javascript"})
    memory.add("Rust is a systems programming language", metadata={"topic": "rust"})
    memory.add("Go is efficient for concurrent programming", metadata={"topic": "go"})
    memory.add("TypeScript adds types to JavaScript", metadata={"topic": "typescript"})
    
    # Search for "programming"
    print("\n2. Search for 'programming':")
    results = memory.search("programming")
    for r in results:
        print(f"   - {r['text']}")
    
    # Search for "language"
    print("\n3. Search for 'language':")
    results = memory.search("language")
    for r in results:
        print(f"   - {r['text']}")
    
    # Search for "web"
    print("\n4. Search for 'web':")
    results = memory.search("web")
    for r in results:
        print(f"   - {r['text']}")
    
    # Get timeline
    print("\n5. Timeline:")
    timeline = memory.get_timeline()
    for t in timeline:
        print(f"   {t['timestamp'][:19]} | {t['text'][:40]}")
    
    # Stats
    print("\n6. Stats:")
    print(f"   Total memories: {memory.count()}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)


if __name__ == "__main__":
    demo_fts()
