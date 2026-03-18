#!/usr/bin/env python3
"""
Agent Memory - Conversation Context
==================================
Build conversation context for chatbots.

Usage:
    from conversation import ConversationContext
    
    ctx = ConversationContext()
    ctx.add_user_message("Hello")
    ctx.add_bot_message("Hi!")
    context = ctx.get_context()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from agent_memory import Memory


class ConversationContext:
    """Conversation context manager."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json", max_turns: int = 10):
        self.memory = Memory(storage=storage, path=path)
        self.max_turns = max_turns
    
    def add_user_message(self, message: str, metadata: dict = None):
        """Add user message."""
        metadata = metadata or {}
        metadata["role"] = "user"
        metadata["type"] = "message"
        
        self.memory.add(f"User: {message}", metadata=metadata)
    
    def add_bot_message(self, message: str, metadata: dict = None):
        """Add bot message."""
        metadata = metadata or {}
        metadata["role"] = "bot"
        metadata["type"] = "message"
        
        self.memory.add(f"Bot: {message}", metadata=metadata)
    
    def get_conversation(self, limit: int = None) -> List[Dict]:
        """Get conversation history."""
        limit = limit or self.max_turns * 2
        
        recent = self.memory.get_recent(limit=limit)
        
        # Filter to just messages
        messages = [m for m in recent if m.get("metadata", {}).get("type") == "message"]
        
        # Reverse to get chronological order
        messages.reverse()
        
        return messages
    
    def get_context(self, max_tokens: int = 1000) -> str:
        """Get context string."""
        conversation = self.get_conversation()
        
        lines = []
        for msg in conversation:
            text = msg["text"]
            role = msg.get("metadata", {}).get("role", "unknown")
            lines.append(f"{role.upper()}: {text}")
        
        context = "\n".join(lines)
        
        # Truncate if needed
        if len(context) > max_tokens * 4:  # Rough estimate
            context = context[-max_tokens * 4:]
        
        return context
    
    def clear_conversation(self):
        """Clear conversation history."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for msg in recent:
            if msg.get("metadata", {}).get("type") == "message":
                self.memory.delete(msg["id"])


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "conversation_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Conversation Context Demo")
    print("=" * 50)
    
    ctx = ConversationContext(storage="json", path=demo_path)
    
    # Simulate conversation
    print("\n1. Simulating conversation...")
    ctx.add_user_message("Hi, I'm looking for a restaurant")
    ctx.add_bot_message("Sure! What type of cuisine do you prefer?")
    ctx.add_user_message("I like Italian food")
    ctx.add_bot_message("Great! There's a nice Italian restaurant nearby. Would you like the address?")
    ctx.add_user_message("Yes, please!")
    ctx.add_bot_message("It's at 123 Main Street. Would you like to make a reservation?")
    
    # Get conversation
    print("\n2. Conversation history:")
    conversation = ctx.get_conversation()
    for msg in conversation:
        print(f"   {msg['text']}")
    
    # Get context
    print("\n3. Context for LLM:")
    context = ctx.get_context()
    print(f"   {context[:200]}...")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
