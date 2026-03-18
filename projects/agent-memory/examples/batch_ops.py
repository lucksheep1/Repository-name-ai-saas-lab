#!/usr/bin/env python3
"""
Agent Memory - Batch Operations
================================
Batch add, search, and export operations.

Usage:
    from batch_ops import batch_add, batch_search
    
    memories = [
        {"text": "Task 1"},
        {"text": "Task 2"},
        {"text": "Task 3"}
    ]
    batch_add(memory, memories)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from agent_memory import Memory


def batch_add(memory: Memory, items: List[Dict[str, Any]]) -> List[str]:
    """Add multiple memories at once."""
    ids = []
    for item in items:
        text = item.get("text", "")
        tags = item.get("tags")
        metadata = item.get("metadata")
        ttl_days = item.get("ttl_days")
        
        if tags:
            memory_id = memory.add_with_tags(text, tags=tags, metadata=metadata)
        else:
            memory_id = memory.add(text, metadata=metadata, ttl_days=ttl_days)
        ids.append(memory_id)
    
    return ids


def batch_search(memory: Memory, queries: List[str], top_k: int = 5) -> Dict[str, List[dict]]:
    """Search for multiple queries at once."""
    results = {}
    for query in queries:
        results[query] = memory.search(query, top_k=top_k)
    return results


def batch_export(memory: Memory, filepath: str, format: str = "json"):
    """Export memory to file."""
    if format == "markdown":
        memory.export_markdown(filepath)
    else:
        memory.export(filepath)


def batch_import(memory: Memory, filepath: str):
    """Import memories from file."""
    memory.import_(filepath)


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "batch_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Batch Operations Demo")
    print("=" * 50)
    
    memory = Memory(storage="json", path=demo_path)
    
    # Batch add
    print("\n1. Batch adding memories...")
    items = [
        {"text": "Remember to buy milk", "tags": ["shopping"]},
        {"text": "Call doctor tomorrow", "tags": ["health"], "metadata": {"priority": 4}},
        {"text": "Finish project report", "tags": ["work"], "metadata": {"priority": 3}},
        {"text": "Water the plants", "tags": ["home"]},
        {"text": "Read chapter 5", "tags": ["reading"]},
    ]
    ids = batch_add(memory, items)
    print(f"   Added {len(ids)} memories")
    
    # Batch search
    print("\n2. Batch searching...")
    queries = ["health", "work", "shopping"]
    results = batch_search(memory, queries)
    for query, hits in results.items():
        print(f"   '{query}': {len(hits)} results")
    
    # Export
    print("\n3. Exporting...")
    export_path = os.path.join(tempfile.gettempdir(), "batch_export.json")
    batch_export(memory, export_path)
    print(f"   Exported to: {export_path}")
    
    # Import to new memory
    print("\n4. Importing to new memory...")
    new_memory = Memory(storage="json", path=demo_path + ".new")
    batch_import(new_memory, export_path)
    print(f"   Imported {new_memory.count()} memories")
    
    # Stats
    print("\n5. Stats:")
    print(f"   Original: {memory.count()} memories")
    print(f"   New: {new_memory.count()} memories")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    if os.path.exists(demo_path):
        os.remove(demo_path)
    if os.path.exists(demo_path + ".new"):
        os.remove(demo_path + ".new")
    if os.path.exists(export_path):
        os.remove(export_path)
