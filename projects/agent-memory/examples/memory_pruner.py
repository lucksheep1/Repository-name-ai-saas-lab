"""
Memory Pruning & Cleanup Utility
Automatically manages memory lifecycle - expires, consolidates, archives
"""
from agent_memory import Memory
import json
import os
from datetime import datetime, timedelta


class MemoryPruner:
    """Utilities for memory maintenance"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_stats(self) -> dict:
        """Get memory statistics"""
        all_memories = self.memory.get_all()
        
        now = datetime.now()
        expired = 0
        recent = 0
        old = 0
        
        for mem in all_memories:
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            age_days = (now - created).days
            
            if age_days > 30:
                old += 1
            elif age_days < 1:
                recent += 1
            
            # Check TTL
            if mem.get("ttl_days"):
                expiry = created + timedelta(days=mem["ttl_days"])
                if now > expiry:
                    expired += 1
        
        return {
            "total": len(all_memories),
            "expired": expired,
            "recent_24h": recent,
            "old_30d": old,
        }
    
    def prune_expired(self) -> int:
        """Remove all expired memories"""
        all_memories = self.memory.get_all()
        now = datetime.now()
        removed = 0
        
        for mem in all_memories:
            if not mem.get("ttl_days"):
                continue
                
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            expiry = created + timedelta(days=mem["ttl_days"])
            
            if now > expiry:
                self.memory.forget(mem["id"])
                removed += 1
        
        return removed
    
    def consolidate_similar(self, threshold: float = 0.8) -> int:
        """Merge similar memories to reduce redundancy"""
        all_memories = self.memory.get_all()
        merged = 0
        
        # Simple word-based similarity
        for i, mem1 in enumerate(all_memories):
            words1 = set(mem1.get("content", "").lower().split())
            
            for mem2 in all_memories[i+1:]:
                words2 = set(mem2.get("content", "").lower().split())
                
                if not words1 or not words2:
                    continue
                    
                overlap = len(words1 & words2) / len(words1 | words2)
                
                if overlap > threshold:
                    # Merge: keep newer, add note about similar
                    new_content = f"{mem1['content']} [Similar to: {mem2['content'][:50]}...]"
                    self.memory.update(mem1["id"], content=new_content)
                    merged += 1
                    break
        
        return merged
    
    def archive_old(self, days: int = 30, archive_path: str = "./archive.json") -> int:
        """Archive old memories to file"""
        all_memories = self.memory.get_all()
        now = datetime.now()
        archived = []
        
        for mem in all_memories:
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            age_days = (now - created).days
            
            if age_days > days:
                archived.append(mem)
                self.memory.forget(mem["id"])
        
        # Save to archive
        if archived:
            existing = []
            if os.path.exists(archive_path):
                with open(archive_path, "r") as f:
                    existing = json.load(f)
            
            with open(archive_path, "w") as f:
                json.dump(existing + archived, f, indent=2)
        
        return len(archived)


def demo():
    """Demo memory pruning"""
    # Create memory with short TTL for demo
    memory = Memory(storage="json", path="./prune_demo.json", ttl_days=1)
    
    # Add memories with different ages (simulated)
    memory.add("Recent memory 1", ttl_days=7)
    memory.add("Recent memory 2", ttl_days=3)
    memory.add("Short TTL memory", ttl_days=0)  # Should expire immediately
    
    # Add via direct DB manipulation to simulate old memories
    import time
    old_time = (datetime.now() - timedelta(days=35)).isoformat()
    
    pruner = MemoryPruner(memory)
    
    print("=== Memory Pruner Demo ===\n")
    
    # Get stats before
    stats = pruner.get_stats()
    print(f"Before pruning:")
    print(f"  Total: {stats['total']}")
    print(f"  Expired: {stats['expired']}\n")
    
    # Prune expired
    removed = pruner.prune_expired()
    print(f"Pruned {removed} expired memories\n")
    
    # Stats after
    stats = pruner.get_stats()
    print(f"After pruning:")
    print(f"  Total: {stats['total']}")
    
    # Cleanup demo file
    if os.path.exists("./prune_demo.json"):
        os.remove("./prune_demo.json")


if __name__ == "__main__":
    demo()
