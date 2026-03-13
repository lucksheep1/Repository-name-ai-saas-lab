#!/usr/bin/env python3
"""
Agent Memory Integration Demo
==============================
This demo shows a minimal agent workflow with memory:
1. Write memory (user input)
2. Retrieve relevant memories
3. Generate context
4. Output response

This simulates a real agent loop: input → store → recall → respond.
"""

import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent_memory import Memory
except ImportError:
    print("Error: agent_memory not installed.")
    print("Install with: pip install -e .")
    sys.exit(1)


def create_agent_with_memory(storage_path: str = "./integration_demo_memory.json"):
    """Create an agent with memory capabilities."""
    
    # Initialize memory with JSON storage
    memory = Memory(storage=storage_path, path=storage_path)
    
    return memory


def demo_workflow():
    """Run a complete workflow demo: add → search → context → output."""
    
    storage_path = "./integration_demo_memory.json"
    
    # Clean up previous demo data
    if os.path.exists(storage_path):
        os.remove(storage_path)
    
    print("=" * 60)
    print("Agent Memory Integration Demo")
    print("=" * 60)
    print()
    
    # Step 1: Initialize agent with memory
    print("Step 1: Initialize agent with memory")
    print("-" * 40)
    memory = create_agent_with_memory(storage_path)
    print(f"✓ Memory initialized: {storage_path}")
    print()
    
    # Step 2: Write memories (simulating agent learning)
    print("Step 2: Write memories (agent learning)")
    print("-" * 40)
    
    memories_to_add = [
        "User prefers dark mode for UI",
        "User's name is Alice",
        "Last project was a Python web app",
        "User is interested in AI agents",
        "User works as a software engineer",
        "Favorite programming language is Python",
        "Currently learning about memory management in AI",
    ]
    
    for i, mem in enumerate(memories_to_add, 1):
        memory.add(mem)
        print(f"  {i}. Stored: '{mem[:40]}...'")
    print()
    
    # Step 3: Retrieve relevant memories (search)
    print("Step 3: Retrieve relevant memories")
    print("-" * 40)
    
    query = "AI agent programming"
    results = memory.search(query)
    print(f"  Query: '{query}'")
    print(f"  Found {len(results)} relevant memories:")
    for r in results:
        print(f"    - {r['text']}")
    print()
    
    # Step 4: Generate context for agent
    print("Step 4: Generate context for agent")
    print("-" * 40)
    
    context = memory.get_context(max_tokens=500)
    print(f"  Context length: {len(context)} chars")
    print(f"  Context preview:")
    print("  " + "-" * 36)
    for line in context[:500].split('\n')[:5]:
        print(f"  {line}")
    print("  ...")
    print()
    
    # Step 5: Simulated agent output
    print("Step 5: Simulated agent output")
    print("-" * 40)
    
    agent_output = f"""
Based on the conversation context:
- User: Alice, a software engineer
- Interests: Python, AI agents, memory management
- Recent work: Python web app project

Agent Response: "I see you're interested in AI agents and memory management! 
Since you're a Python developer working on a web app, you'd probably benefit 
from agent-memory - a lightweight library for managing agent context. 
It integrates well with LangChain and can help your agents remember 
user preferences like dark mode across sessions."
"""
    print(agent_output)
    
    # Step 6: Remember the agent's response
    print("Step 6: Remember agent's response")
    print("-" * 40)
    
    memory.add("Agent recommended agent-memory library for AI agent context management")
    print("  ✓ Agent response stored in memory")
    print()
    
    # Step 7: Verify timeline
    print("Step 7: Timeline view")
    print("-" * 40)
    
    timeline = memory.get_timeline(limit=5)
    print(f"  Recent {len(timeline)} memories:")
    for item in timeline:
        print(f"    [{item['created_at']}] {item['text'][:50]}...")
    print()
    
    # Summary
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("This demo demonstrated:")
    print("  1. ✓ Write memory (add)")
    print("  2. ✓ Retrieve (search)")
    print("  3. ✓ Generate context (get_context)")
    print("  4. ✓ Output response")
    print("  5. ✓ Remember response")
    print("  6. ✓ Timeline view")
    print()
    print(f"Memory file: {storage_path}")
    print("You can inspect it with: cat ./integration_demo_memory.json")
    
    return True


if __name__ == "__main__":
    success = demo_workflow()
    sys.exit(0 if success else 1)
