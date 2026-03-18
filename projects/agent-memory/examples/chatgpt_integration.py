#!/usr/bin/env python3
"""
Agent Memory - ChatGPT/GPT API Integration
==========================================
Use agent-memory with OpenAI's ChatGPT API.

Usage:
    pip install openai
    export OPENAI_API_KEY="your-key"
    python chatgpt_integration.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


def get_openai_client():
    """Get OpenAI client."""
    if not HAS_OPENAI:
        return None
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def build_messages(memory, user_message):
    """Build messages with memory context."""
    # Get relevant memories
    relevant = memory.search(user_message, top_k=3)
    
    # Build system prompt with context
    context_parts = ["You are a helpful assistant with memory."]
    
    if relevant:
        context_parts.append("\nRelevant context from memory:")
        for mem in relevant:
            context_parts.append(f"- {mem['text']}")
    
    system_prompt = "\n".join(context_parts)
    
    # Get recent conversation
    recent = memory.get_recent(limit=6)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent conversation
    for mem in recent:
        role = mem.get("metadata", {}).get("role", "user")
        messages.append({"role": role, "content": mem["text"]})
    
    # Add current message
    messages.append({"role": "user", "content": user_message})
    
    return messages


def chat(memory, user_message, model="gpt-4"):
    """
    Chat with ChatGPT using memory context.
    """
    client = get_openai_client()
    
    # Store user message
    memory.add(user_message, metadata={"role": "user", "source": "chatgpt"})
    
    # Build messages
    messages = build_messages(memory, user_message)
    
    if client:
        # Call OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
    else:
        # Demo mode
        reply = f"ChatGPT demo: processed '{user_message[:30]}...'"
    
    # Store assistant response
    memory.add(reply, metadata={"role": "assistant", "source": "chatgpt"})
    
    return reply


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "chatgpt_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    memory = Memory(storage="json", path=demo_path)
    
    print("🤖 Agent Memory - ChatGPT Integration Demo")
    print("=" * 50)
    
    if not HAS_OPENAI:
        print("⚠️ openai not installed. Running in demo mode.")
    
    # Seed memory
    memory.add("User is named Sarah", metadata={"role": "system", "source": "chatgpt"})
    memory.add("User works as a data scientist", metadata={"role": "system", "source": "chatgpt"})
    memory.add("User loves machine learning", metadata={"role": "system", "source": "chatgpt"})
    
    # Chat
    print("\n1. Hello, what's my name?")
    reply = chat(memory, "Hello, what's my name?")
    print(f"   → {reply}")
    
    print("\n2. What do I do for work?")
    reply = chat(memory, "What do I do for work?")
    print(f"   → {reply}")
    
    print("\n3. What do I love?")
    reply = chat(memory, "What do I love?")
    print(f"   → {reply}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
