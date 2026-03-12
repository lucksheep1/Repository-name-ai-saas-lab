"""
Multi-Agent Memory Sharing Example

Shows how multiple agents can share memory through a central store.
Useful for distributed AI systems.
"""
import json
from agent_memory import Memory
from datetime import datetime

# Shared memory store (could be Redis, PostgreSQL, etc.)
SHARED_MEMORY_PATH = "./shared_memory.json"

# Initialize shared memory
shared_memory = Memory(storage="json", path=SHARED_MEMORY_PATH)

# Agent 1: User Interface Agent
def agent_ui():
    """UI agent handles user interactions."""
    shared_memory.add(
        "UI Agent: User asked about pricing plans",
        metadata={"agent": "ui", "topic": "pricing"}
    )
    shared_memory.add_with_tags(
        "User email: user@example.com",
        tags=["user-data", "ui"]
    )
    print("✓ UI Agent logged interaction")

# Agent 2: Technical Agent  
def agent_tech():
    """Technical agent handles implementation details."""
    shared_memory.add(
        "Tech Agent: Implemented OAuth2 authentication",
        metadata={"agent": "tech", "topic": "auth"}
    )
    shared_memory.add_with_tags(
        "Tech Agent: Database schema updated for user profiles",
        tags=["database", "tech"]
    )
    print("✓ Tech Agent logged work")

# Agent 3: Analytics Agent
def agent_analytics():
    """Analytics agent tracks usage patterns."""
    # Search for relevant memories
    auth_related = shared_memory.search("authentication")
    print(f"\n=== Analytics: Found {len(auth_related)} auth-related memories ===")
    
    # Get all by agent
    ui_memories = shared_memory.search("UI Agent")
    tech_memories = shared_memory.search("Tech Agent")
    
    print(f"UI memories: {len(ui_memories)}")
    print(f"Tech memories: {len(tech_memories)}")
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_memories": len(shared_memory.memories),
        "by_agent": {
            "ui": len(ui_memories),
            "tech": len(tech_memories)
        }
    }
    print(f"\n=== Analytics Report ===")
    print(json.dumps(report, indent=2))
    
    shared_memory.add(
        f"Analytics: Generated report - {report['total_memories']} total memories",
        metadata={"agent": "analytics"}
    )

# Run all agents
print("=== Multi-Agent Memory Demo ===\n")
agent_ui()
agent_tech()
agent_analytics()

# Export shared memory
shared_memory.export("shared_memory.json")
print("\n✓ Shared memory exported")

# Show timeline
print("\n=== Shared Memory Timeline ===")
timeline = shared_memory.get_timeline()
for item in timeline[:5]:
    print(f"- {item['timestamp']}: {item['text'][:50]}...")
