"""
Memory Version Control
Track changes to memories over time
"""
from agent_memory import Memory
import json
from datetime import datetime


class VersionedMemory:
    """Memory with version control"""
    
    def __init__(self, memory: Memory, versions_path: str = "./versions"):
        self.memory = memory
        self.versions_path = versions_path
        self.versions = {}  # mem_id -> list of versions
    
    def add(self, content: str, **kwargs):
        """Add with versioning"""
        mem_id = self.memory.add(content, **kwargs)
        
        # Store initial version
        self._save_version(mem_id, content, "create")
        
        return mem_id
    
    def update(self, mem_id: str, **updates):
        """Update with versioning"""
        # Get current
        mem = self.memory.get(mem_id)
        if not mem:
            return None
        
        # Save current as new version
        self._save_version(mem_id, mem.get("content", ""), "update")
        
        # Apply update
        result = self.memory.update(mem_id, **updates)
        
        # Save new version
        updated = self.memory.get(mem_id)
        self._save_version(mem_id, updated.get("content", ""), "update")
        
        return result
    
    def forget(self, mem_id: str):
        """Delete with versioning"""
        mem = self.memory.get(mem_id)
        
        if mem:
            self._save_version(mem_id, mem.get("content", ""), "delete")
        
        return self.memory.forget(mem_id)
    
    def _save_version(self, mem_id: str, content: str, action: str):
        """Save a version"""
        if mem_id not in self.versions:
            self.versions[mem_id] = []
        
        self.versions[mem_id].append({
            "content": content,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_history(self, mem_id: str) -> list:
        """Get version history"""
        return self.versions.get(mem_id, [])
    
    def restore(self, mem_id: str, version_index: int) -> bool:
        """Restore to a specific version"""
        history = self.get_history(mem_id)
        
        if 0 <= version_index < len(history):
            version = history[version_index]
            self.memory.update(mem_id, content=version["content"])
            return True
        
        return False


class DiffViewer:
    """Compare memory versions"""
    
    @staticmethod
    def diff(v1: str, v2: str) -> dict:
        """Simple diff between two versions"""
        words1 = v1.split()
        words2 = v2.split()
        
        added = set(words2) - set(words1)
        removed = set(words1) - set(words2)
        
        return {
            "added": list(added),
            "removed": list(removed),
            "unchanged": list(set(words1) & set(words2))
        }


def demo():
    """Demo version control"""
    memory = Memory(storage="json", path="./version_demo.json")
    vmem = VersionedMemory(memory)
    
    print("=== Versioned Memory Demo ===\n")
    
    # Add
    mem_id = vmem.add("Initial content: Hello world")
    print(f"Added memory: {mem_id}")
    
    # Update
    vmem.update(mem_id, content="Updated: Hello world, welcome!")
    print("Updated memory")
    
    # Get history
    history = vmem.get_history(mem_id)
    print(f"\nVersion history ({len(history)} versions):")
    for i, v in enumerate(history):
        print(f"  {i}: {v['action']} at {v['timestamp'][:19]}")
        print(f"      {v['content'][:50]}")
    
    # Show diff
    if len(history) >= 2:
        diff = DiffViewer.diff(history[0]["content"], history[-1]["content"])
        print(f"\nDiff:")
        print(f"  Added: {diff['added']}")
        print(f"  Removed: {diff['removed']}")
    
    # Cleanup
    import os
    if os.path.exists("./version_demo.json"):
        os.remove("./version_demo.json")


if __name__ == "__main__":
    demo()
