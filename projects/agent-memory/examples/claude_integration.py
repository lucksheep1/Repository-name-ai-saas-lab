#!/usr/bin/env python3
"""
Agent Memory - Anthropic Claude Integration
===========================================
Use agent-memory with Anthropic's Claude API.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-key"
    python claude_integration.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def get_claude_client():
    """Get Anthropic client."""
    if not HAS_ANTHROPIC:
        return None
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def build_prompt(memory, user_message):
    """Build prompt with memory context."""
    # Get relevant memories
    relevant = memory.search(user_message, top_k=3)
    
    # Build context
    context_parts = []
    
    if relevant:
        context_parts.append("Relevant context from memory:")
        for mem in relevant:
            context_parts.append(f"- {mem['text']}")
    
    context_str = "\n".join(context_parts) if context_parts else "No relevant context."
    
    # Get recent conversation
    recent = memory.get_recent(limit=8)
    conversation = "\n".join([
        f"{mem.get('metadata', {}).get('role', 'user')}: {mem['text']}"
        for mem in recent
    ])
    
    prompt = f"""<context>
{context_str}
</context>

<recent_conversation>
{conversation}
</recent_conversation>

User: {user_message}
Assistant: """
    
    return prompt


def chat(memory, user_message, model="claude-3-opus-20240229"):
    """
    Chat with Claude using memory context.
    """
    client = get_claude_client()
    
    # Store user message
    memory.add(user_message, metadata={"role": "user", "source": "claude"})
    
    # Build prompt
    prompt = build_prompt(memory, user_message)
    
    if client:
        # Call Anthropic
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            prompt=prompt
        )
        reply = response.completion.strip()
    else:
        # Demo mode
        reply = f"Claude demo: processed '{user_message[:30]}...'"
    
    # Store assistant response
    memory.add(reply, metadata={"role": "assistant", "source": "claude"})
    
    return reply


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "claude_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    memory = Memory(storage="json", path=demo_path)
    
    print("🤖 Agent Memory - Claude Integration Demo")
    print("=" * 50)
    
    if not HAS_ANTHROPIC:
        print("⚠️ anthropic not installed. Running in demo mode.")
    
    # Seed memory
    memory.add("User is named Mike", metadata={"role": "system", "source": "claude"})
    memory.add("User lives in San Francisco", metadata={"role": "system", "source": "claude"})
    memory.add("User develops AI applications", metadata={"role": "system", "source": "claude"})
    
    # Chat
    print("\n1. Hi! What's my name?")
    reply = chat(memory, "Hi! What's my name?")
    print(f"   → {reply}")
    
    print("\n2. Where do I live?")
    reply = chat(memory, "Where do I live?")
    print(f"   → {reply}")
    
    print("\n3. What do I develop?")
    reply = chat(memory, "What do I develop?")
    print(f"   → {reply}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
