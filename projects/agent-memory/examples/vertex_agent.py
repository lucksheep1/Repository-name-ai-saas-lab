#!/usr/bin/env python3
"""
Agent Memory - Vertex AI Agent (Google Cloud)
=============================================
Use agent-memory with Google Cloud's Vertex AI Agent.

Usage:
    pip install google-cloud-aiplatform
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
    python vertex_agent.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


def build_context(memory, query, max_tokens=2000):
    """Build context for Vertex AI prompt."""
    relevant = memory.search(query, top_k=5)
    recent = memory.get_recent(limit=10)
    
    context = {
        "relevant_memories": relevant,
        "recent_conversation": recent,
        "context_string": memory.get_context(max_tokens=max_tokens)
    }
    return context


def chat_with_vertex(memory, user_input):
    """
    Chat with Vertex AI Agent using memory context.
    
    In production, integrate with actual Vertex AI API.
    """
    # Store user message
    memory.add(f"User: {user_input}", metadata={"role": "user", "source": "vertex"})
    
    # Build context
    context = build_context(memory, user_input)
    
    print(f"\n📋 Context for Vertex AI:")
    print(f"  Relevant: {len(context['relevant_memories'])} memories")
    print(f"  Recent: {len(context['recent_conversation'])} messages")
    
    # In production: call Vertex AI with context
    # response = vertexai.generate_response(context)
    
    # Simulate response
    response = f"Processed with context: {user_input[:30]}..."
    
    # Store response
    memory.add(f"Agent: {response}", metadata={"role": "agent", "source": "vertex"})
    
    return response


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "vertex_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    memory = Memory(storage="json", path=demo_path)
    
    print("🤖 Agent Memory - Vertex AI Demo")
    print("=" * 50)
    
    # Seed memory
    memory.add("User prefers Japanese food", metadata={"role": "system"})
    memory.add("User lives in Tokyo", metadata={"role": "system"})
    memory.add("User is a software engineer", metadata={"role": "system"})
    
    # Chat
    chat_with_vertex(memory, "What food do I like?")
    chat_with_vertex(memory, "Where do I live?")
    chat_with_vertex(memory, "What is my job?")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
