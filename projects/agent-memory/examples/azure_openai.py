#!/usr/bin/env python3
"""
Agent Memory - Azure OpenAI Integration
========================================
Use agent-memory with Azure OpenAI.

Usage:
    pip install openai
    export AZURE_OPENAI_KEY="your-key"
    export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
    python azure_openai.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


try:
    from openai import AzureOpenAI
    HAS_AZURE = True
except ImportError:
    HAS_AZURE = False


def get_azure_client():
    """Get Azure OpenAI client."""
    if not HAS_AZURE:
        return None
    
    return AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )


def build_prompt(memory, user_query, system_prompt=None):
    """Build prompt with memory context."""
    context = memory.get_context(max_tokens=1500)
    
    prompt_parts = []
    if system_prompt:
        prompt_parts.append(system_prompt)
    
    prompt_parts.append(f"\nRelevant context:\n{context}")
    prompt_parts.append(f"\nUser query: {user_query}")
    
    return "\n".join(prompt_parts)


def chat_with_azure(memory, user_input, model="gpt-4"):
    """
    Chat with Azure OpenAI using memory context.
    """
    client = get_azure_client()
    
    # Store user message
    memory.add(f"User: {user_input}", metadata={"role": "user", "source": "azure"})
    
    # Build prompt
    prompt = build_prompt(memory, user_input)
    
    if client:
        # Call Azure OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant with memory."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
    else:
        # Demo mode
        reply = f"Azure OpenAI demo: processed '{user_input}'"
    
    # Store response
    memory.add(f"Assistant: {reply}", metadata={"role": "assistant", "source": "azure"})
    
    return reply


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "azure_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    memory = Memory(storage="json", path=demo_path)
    
    print("🤖 Agent Memory - Azure OpenAI Demo")
    print("=" * 50)
    
    if not HAS_AZURE:
        print("⚠️ openai not installed. Running in demo mode.")
    
    # Seed memory
    memory.add("User's name is Alex", metadata={"role": "system"})
    memory.add("User works at Acme Corp", metadata={"role": "system"})
    memory.add("User likes coffee", metadata={"role": "system"})
    
    # Chat
    print("\n1. Query: What's my name?")
    reply = chat_with_azure(memory, "What's my name?")
    print(f"   Response: {reply}")
    
    print("\n2. Query: Where do I work?")
    reply = chat_with_azure(memory, "Where do I work?")
    print(f"   Response: {reply}")
    
    print("\n3. Query: What do I like?")
    reply = chat_with_azure(memory, "What do I like?")
    print(f"   Response: {reply}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
