#!/usr/bin/env python3
"""
Agent Memory v3.1 - 30 Second Demo
===================================
v3.1: String TTL + Encryption + Redis

Copy, paste, run - that's it!
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_memory import Memory

def run_demo():
    print("=" * 50)
    print("⚡ Agent Memory v3.1 - 30 Second Demo")
    print("=" * 50)
    
    demo_path = "/tmp/agent_memory_demo.json"
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    # v3.1: String TTL + Encryption
    memory = Memory(storage="json", path=demo_path, ttl="7d", encryption_key="demo_key_32bytes_xxxxxxx")
    
    # 1. Basic memory
    print("\n1. Adding memories...")
    memory.add("User prefers dark mode")
    memory.add("Building an AI agent startup")
    
    # 2. String TTL - auto-expire after 1 hour
    temp_id = memory.add("Temporary session data", ttl="1h")
    print(f"   Added with ttl=1h (id: {temp_id})")
    
    # 3. Encryption for sensitive data
    memory.add("sk-xxxx-secret-key", encrypt=True)
    print("   Added encrypted secret key")
    
    # 4. Search
    print("\n2. Searching memories...")
    results = memory.search("AI agent")
    print(f"   Found {len(results)} matching memories")
    
    # 5. TTL query
    print("\n3. TTL remaining:")
    rem = memory.ttl_remaining(temp_id)
    print(f"   {temp_id}: {rem:.0f}s until expiry")
    
    # 6. Context retrieval
    print("\n4. Context retrieval:")
    context = memory.get_context(max_tokens=300)
    print(f"   Retrieved context ({len(context)} chars)")
    
    print("\n" + "=" * 50)
    print("📢 v3.1 Features:")
    print("   • String TTL: '1h', '30m', '7d', '2w'")
    print("   • Encryption: Memory.add(text, encrypt=True)")
    print("   • Redis backend: Memory(storage='redis', redis_url='...')")
    print("=" * 50)
    print("\n👉 GitHub: github.com/lucksheep1/Repository-name-ai-saas-lab")
    print("   Give feedback: Open an issue!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)

if __name__ == "__main__":
    run_demo()
