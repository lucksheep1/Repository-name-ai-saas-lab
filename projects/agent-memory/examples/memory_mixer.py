#!/usr/bin/env python3
"""
Agent Memory - Memory Mixer
===========================
Combine multiple memory sources into one unified context.

This is useful when you have:
- User profile memories
- Conversation history
- Task-specific memories

Usage:
    from memory_mixer import MemoryMixer
    
    mixer = MemoryMixer()
    mixer.add_source("profile", profile_memory)
    mixer.add_source("chat", chat_memory)
    mixer.add_source("tasks", task_memory)
    
    context = mixer.get_unified_context("What was the last task?")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from agent_memory import Memory


class MemoryMixer:
    """Combine multiple memory sources."""
    
    def __init__(self):
        self.sources: Dict[str, Memory] = {}
        self.weights: Dict[str, float] = {}
    
    def add_source(self, name: str, memory: Memory, weight: float = 1.0):
        """Add a memory source with optional weight."""
        self.sources[name] = memory
        self.weights[name] = weight
    
    def remove_source(self, name: str):
        """Remove a memory source."""
        if name in self.sources:
            del self.sources[name]
            del self.weights[name]
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search across all sources."""
        results = []
        
        for name, memory in self.sources.items():
            weight = self.weights.get(name, 1.0)
            source_results = memory.search(query, top_k=top_k)
            
            for result in source_results:
                result["_source"] = name
                result["_weight"] = weight
                results.append(result)
        
        # Sort by weight
        results.sort(key=lambda x: x.get("_weight", 1.0), reverse=True)
        
        return results[:top_k]
    
    def get_unified_context(self, query: str, max_tokens: int = 2000) -> str:
        """Get unified context from all sources."""
        relevant = self.search(query, top_k=10)
        
        if not relevant:
            return "No relevant memories found."
        
        # Group by source
        by_source: Dict[str, List[str]] = {}
        for mem in relevant:
            source = mem.get("_source", "unknown")
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(mem["text"])
        
        # Build context
        parts = ["Context from memory sources:"]
        
        for source, texts in by_source.items():
            parts.append(f"\n[{source}]")
            for text in texts:
                parts.append(f"  - {text}")
        
        return "\n".join(parts)
    
    def get_all_recent(self, limit: int = 10) -> Dict[str, List[dict]]:
        """Get recent memories from all sources."""
        recent = {}
        
        for name, memory in self.sources.items():
            recent[name] = memory.get_recent(limit=limit)
        
        return recent
    
    def get_stats(self) -> Dict[str, dict]:
        """Get statistics for all sources."""
        stats = {}
        
        for name, memory in self.sources.items():
            stats[name] = {
                "count": memory.count(),
                "weight": self.weights.get(name, 1.0)
            }
        
        return stats


# Demo
if __name__ == "__main__":
    import tempfile
    
    print("🤖 Agent Memory - Memory Mixer Demo")
    print("=" * 50)
    
    # Create separate memory stores
    profile_path = os.path.join(tempfile.gettempdir(), "mixer_profile.json")
    chat_path = os.path.join(tempfile.gettempdir(), "mixer_chat.json")
    tasks_path = os.path.join(tempfile.gettempdir(), "mixer_tasks.json")
    
    # Clean up
    for p in [profile_path, chat_path, tasks_path]:
        if os.path.exists(p):
            os.remove(p)
    
    # Create memories
    profile_mem = Memory(storage="json", path=profile_path)
    chat_mem = Memory(storage="json", path=chat_path)
    tasks_mem = Memory(storage="json", path=tasks_path)
    
    # Seed profile memory
    profile_mem.add("User name: Alice", metadata={"source": "profile"})
    profile_mem.add("User role: Software Engineer", metadata={"source": "profile"})
    profile_mem.add("User prefers TypeScript", metadata={"source": "profile"})
    
    # Seed chat memory
    chat_mem.add("User said: Hello!", metadata={"source": "chat"})
    chat_mem.add("Assistant: Hi! How can I help?", metadata={"source": "chat"})
    chat_mem.add("User said: I'm working on a web app", metadata={"source": "chat"})
    
    # Seed tasks memory
    tasks_mem.add("Task: Fix login bug", metadata={"source": "tasks", "priority": 5})
    tasks_mem.add("Task: Add dark mode", metadata={"source": "tasks", "priority": 3})
    tasks_mem.add("Task: Write tests", metadata={"source": "tasks", "priority": 2})
    
    # Create mixer
    mixer = MemoryMixer()
    mixer.add_source("profile", profile_mem, weight=2.0)
    mixer.add_source("chat", chat_mem, weight=1.0)
    mixer.add_source("tasks", tasks_mem, weight=1.5)
    
    # Search
    print("\n1. Search for 'user':")
    results = mixer.search("user")
    for r in results:
        print(f"   [{r['_source']}] {r['text']}")
    
    print("\n2. Search for 'task':")
    results = mixer.search("task")
    for r in results:
        print(f"   [{r['_source']}] {r['text']}")
    
    print("\n3. Unified context for 'preferences':")
    context = mixer.get_unified_context("preferences")
    print(context)
    
    print("\n4. Stats:")
    stats = mixer.get_stats()
    for name, s in stats.items():
        print(f"   {name}: {s['count']} memories, weight={s['weight']}")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    for p in [profile_path, chat_path, tasks_path]:
        if os.path.exists(p):
            os.remove(p)
