#!/usr/bin/env python3
"""
Agent Memory - OpenAI Assistant Integration
============================================
Use agent-memory with OpenAI Assistants API for persistent context.

This example shows how to maintain conversation context across
multiple sessions using agent-memory as the memory layer.

Usage:
    python openai_assistant.py
    
Requirements:
    pip install openai
    export OPENAI_API_KEY="your-key"
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory

# Check for OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


def create_assistant_memory(storage="json", path="./assistant_memory.json"):
    """Create memory instance for assistant."""
    return Memory(storage=storage, path=path)


def build_context_for_prompt(memory, user_query, max_tokens=2000):
    """
    Build context for the assistant prompt.
    
    This retrieves relevant memories and formats them as context.
    """
    # Search for relevant memories
    relevant = memory.search(user_query, top_k=5)
    
    # Get high priority items
    important = memory.get_by_priority(4)
    
    # Get recent conversation context
    recent = memory.get_recent(limit=10)
    
    # Build context string
    context_parts = []
    
    if relevant:
        context_parts.append("Relevant memories:")
        for mem in relevant:
            context_parts.append(f"  - {mem['text']}")
    
    if important:
        context_parts.append("\nImportant items:")
        for mem in important:
            context_parts.append(f"  - {mem['text']}")
    
    if recent:
        context_parts.append("\nRecent conversation:")
        for mem in recent:
            context_parts.append(f"  - {mem['text']}")
    
    return "\n".join(context_parts) if context_parts else "No context available."


def chat_with_memory(memory, user_input, system_prompt=None):
    """
    Simple chat with memory integration.
    
    For production, integrate with actual LLM API.
    """
    # Store user message
    memory.add(f"User: {user_input}", metadata={"role": "user"})
    
    # Build context
    context = build_context_for_prompt(memory, user_input)
    
    # In production, this would call the LLM
    # For demo, just show the context
    print(f"\n📋 Context for assistant:")
    print("-" * 40)
    print(context[:500] if len(context) > 500 else context)
    print("-" * 40)
    
    # Simulate response (replace with actual LLM call)
    response = f"Processed: {user_input[:50]}..."
    memory.add(f"Assistant: {response}", metadata={"role": "assistant"})
    
    return response


# Demo
if __name__ == "__main__":
    import tempfile
    
    # Use temp file for demo
    demo_path = os.path.join(tempfile.gettempdir(), "assistant_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    memory = create_assistant_memory(path=demo_path)
    
    print("=" * 50)
    print("🤖 Agent Memory - OpenAI Assistant Demo")
    print("=" * 50)
    
    # Seed with some context
    print("\n1. Seeding memory with initial context...")
    memory.add("User prefers dark mode", metadata={"role": "system", "priority": 3})
    memory.add("User is building AI agents", metadata={"role": "system", "priority": 4})
    memory.add("User likes Python", metadata={"role": "system", "priority": 2})
    
    # Simulate conversation
    print("\n2. Simulating conversation...")
    
    chat_with_memory(memory, "What's my name?")
    chat_with_memory(memory, "What do I like?")
    chat_with_memory(memory, "What am I building?")
    
    # Show timeline
    print("\n3. Memory timeline:")
    timeline = memory.get_timeline(limit=5)
    for item in timeline:
        print(f"  {item['timestamp'][:19]}: {item['text'][:50]}")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    if os.path.exists(demo_path):
        os.remove(demo_path)
