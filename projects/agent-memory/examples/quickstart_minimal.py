#!/usr/bin/env python3
"""
Agent Memory Manager - Minimal Quick Start

This is the simplest possible example - just 3 lines to get started!
"""

# 1. Install: pip install agent-memory

# 2. Use (just 3 lines!)
from agent_memory import Memory
memory = Memory()  # Uses JSON storage by default
memory.add("Hello, world!")

# 3. Get context for your AI agent
context = memory.get_context(max_tokens=1000)
print(context)

# That's it! Your agent now has memory.

# --- Want more? ---

# Add with tags
memory.add_with_tags("User likes dark mode", tags=["preference", "ui"])

# Search memories
results = memory.search("user preference")
print(results)

# Get context (enhanced)
context = memory.get_context(max_tokens=2000)
print(context)

# --- For more examples, see: ---
# - langchain_example.py   (LangChain integration)
# - multi_agent_example.py (Multi-agent sharing)
# - api_server.py          (FastAPI server)
# - integration_demo.py    (Complete workflow)

print("\n→ See more examples in the examples/ folder!")
