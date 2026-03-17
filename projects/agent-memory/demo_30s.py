#!/usr/bin/env python3
"""
Agent Memory - 30 Second Demo
=============================
Copy, paste, run - that's it!

This demo shows the simplest possible memory usage.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_memory import Memory

def run_demo():
    print("=" * 50)
    print("⚡ Agent Memory - 30 Second Demo")
    print("=" * 50)
    
    # Use temp file for demo
    demo_path = "/tmp/agent_memory_demo.json"
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    # Create memory with JSON storage
    memory = Memory(storage="json", path=demo_path)
    
    # Add some sample memories
    print("\n1. Adding memories...")
    memory.add("User prefers dark mode", metadata={"source": "demo"})
    memory.add("User is building an AI agent", metadata={"source": "demo"})
    memory.add("User needs simple memory management", metadata={"source": "demo"})
    
    # Get context
    print("2. Getting context...")
    context = memory.get_context(max_tokens=500)
    
    print("\n" + "=" * 50)
    print("CONTEXT FOR YOUR AGENT:")
    print("=" * 50)
    print(context)
    print("=" * 50)
    
    # Search demo
    print("\n3. Searching memories...")
    results = memory.search("AI agent")
    print(f"Found {len(results)} matching memories")
    
    print("\n✅ Demo complete!")
    print("\n" + "=" * 50)
    print("📢 FEEDBACK TIME!")
    print("=" * 50)
    print("Is LangChain memory too heavy for you?")
    print("Do you need agent memory right now?")
    print("Would you try a demo if it took 30 seconds?")
    print("\n👉 Give feedback:")
    print("   https://github.com/lucksheep1/Repository-name-ai-saas-lab/issues")
    print("=" * 50)
    
    # Cleanup
    if os.path.exists(demo_path):
        os.remove(demo_path)

if __name__ == "__main__":
    run_demo()
