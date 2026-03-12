#!/usr/bin/env python3
"""
Agent Memory Manager - Quick Start Example

This script demonstrates the basic usage of agent-memory.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


def main():
    """Run a quick demonstration of agent-memory features."""
    
    # Initialize memory with JSON storage
    print("Initializing memory...")
    memory = Memory(storage="json", path="./demo_memory.json")
    
    # Clear any existing data
    memory.clear()
    print("✓ Memory initialized and cleared\n")
    
    # Add some basic memories
    print("Adding memories...")
    memory.add("User prefers dark mode")
    memory.add("User's name is John")
    memory.add("Working on a Python project")
    print("✓ Added 3 basic memories\n")
    
    # Add memories with tags
    print("Adding tagged memories...")
    memory.add_with_tags("Bug in login", tags=["bug", "urgent"])
    memory.add_with_tags("New feature idea", tags=["feature", "enhancement"])
    memory.add_with_tags("User feedback received", tags=["feedback"])
    print("✓ Added 3 tagged memories\n")
    
    # Add memories with priority
    print("Adding prioritized memories...")
    memory.add("Low priority task", metadata={"priority": 1})
    memory.add("Medium priority task", metadata={"priority": 3})
    memory.add("Critical production issue", metadata={"priority": 5})
    print("✓ Added 3 prioritized memories\n")
    
    # Search memories
    print("Searching for 'user'...")
    results = memory.search("user")
    for r in results:
        print(f"  - {r['text']}")
    print()
    
    # Get by tag
    print("Getting memories tagged 'bug'...")
    bugs = memory.get_by_tag("bug")
    for b in bugs:
        print(f"  - {b['text']}")
    print()
    
    # Get by priority
    print("Getting high priority memories (≥4)...")
    important = memory.get_by_priority(4)
    for i in important:
        print(f"  - {i['text']} (priority: {i.get('metadata', {}).get('priority', 'N/A')})")
    print()
    
    # Get context
    print("Getting context for AI agent...")
    context = memory.get_context(max_tokens=500)
    print(context[:500] + "..." if len(context) > 500 else context)
    print()
    
    # Get timeline
    print("Getting timeline...")
    timeline = memory.get_timeline(limit=5)
    for t in timeline:
        print(f"  - {t['created_at']}: {t['text'][:50]}...")
    print()
    
    # Get statistics
    print("Getting statistics...")
    stats = memory.count()
    print(f"  Total memories: {stats}")
    print()
    
    # Export
    print("Exporting to JSON...")
    memory.export("demo_backup.json")
    print("✓ Exported to demo_backup.json")
    
    print("Exporting to Markdown...")
    memory.export_markdown("demo_memory.md")
    print("✓ Exported to demo_memory.md\n")
    
    print("Demo completed! ✓")


if __name__ == "__main__":
    main()
