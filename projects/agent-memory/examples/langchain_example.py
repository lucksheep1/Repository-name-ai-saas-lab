"""
Agent Memory with LangChain Integration Example

Shows how to use agent-memory with LangChain for conversation context.
"""
import json
from agent_memory import Memory

# Initialize memory
memory = Memory(storage="json", path="./memory_langchain.json")

# Simulate a conversation with context
conversation_history = [
    {"role": "user", "content": "I want to build a chatbot that remembers user preferences"},
    {"role": "assistant", "content": "Great! What kind of preferences do you want to store?"},
    {"role": "user", "content": "Theme preference, language, and notification settings"},
]

# Add conversation to memory
for msg in conversation_history:
    memory.add(
        f"{msg['role']}: {msg['content']}",
        metadata={"role": msg["role"], "priority": 1}
    )

# Add user preference explicitly
memory.add_with_tags(
    "User: prefers dark theme, Chinese language, email notifications",
    tags=["preference", "user-settings"]
)
memory.add_with_tags(
    "User: interested in AI agents and developer tools",
    tags=["interest", "ai-tools"]
)

# Get context for LLM
context = memory.get_context(max_tokens=500)
print("=== Context for LLM ===")
print(context)

# Search relevant memories
print("\n=== Search: theme ===")
results = memory.search("theme")
for r in results:
    print(f"- {r['text']}")

# Get by tag
print("\n=== Get by tag: preference ===")
prefs = memory.get_by_tag("preference")
for p in prefs:
    print(f"- {p['text']}")

# Export for debugging
memory.export("langchain_integration_demo.json")
print("\n✓ Exported to langchain_integration_demo.json")
