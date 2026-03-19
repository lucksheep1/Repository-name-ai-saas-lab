"""
Memory Analytics Dashboard
Real-time memory usage statistics and insights
"""
from agent_memory import Memory
import json
from collections import Counter
from datetime import datetime, timedelta


class MemoryAnalytics:
    """Analytics for memory usage patterns"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_summary(self) -> dict:
        """Get comprehensive summary"""
        all_memories = self.memory.get_all()
        
        if not all_memories:
            return {"total": 0, "message": "No memories"}
        
        # Time-based stats
        now = datetime.now()
        created_times = []
        
        for mem in all_memories:
            try:
                created = datetime.fromisoformat(mem.get("created_at", ""))
                created_times.append(created)
            except:
                pass
        
        # Tag analysis
        tags = []
        for mem in all_memories:
            tags.extend(mem.get("tags", []))
        
        tag_counts = Counter(tags).most_common(10)
        
        # Priority distribution
        priorities = Counter(m.get("priority", "none") for m in all_memories)
        
        return {
            "total_memories": len(all_memories),
            "oldest_memory": min(created_times).isoformat() if created_times else None,
            "newest_memory": max(created_times).isoformat() if created_times else None,
            "top_tags": [{"tag": t, "count": c} for t, c in tag_counts],
            "priority_distribution": dict(priorities),
        }
    
    def get_timeline(self, days: int = 7) -> list:
        """Get memory creation timeline"""
        all_memories = self.memory.get_all()
        
        timeline = []
        now = datetime.now()
        
        for mem in all_memories:
            try:
                created = datetime.fromisoformat(mem.get("created_at", ""))
                age_days = (now - created).days
                
                if age_days <= days:
                    timeline.append({
                        "content": mem.get("content", "")[:100],
                        "created_at": mem.get("created_at"),
                        "age_days": age_days,
                        "tags": mem.get("tags", []),
                    })
            except:
                pass
        
        return sorted(timeline, key=lambda x: x["age_days"])
    
    def get_tag_cooccurrence(self) -> dict:
        """Find which tags often appear together"""
        cooccur = Counter()
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            if len(tags) > 1:
                # All pairs
                for i, t1 in enumerate(tags):
                    for t2 in tags[i+1:]:
                        pair = tuple(sorted([t1, t2]))
                        cooccur[pair] += 1
        
        return {f"{t1}+{t2}": count for (t1, t2), count in cooccur.most_common(10)}


def demo():
    """Demo analytics"""
    memory = Memory(storage="json", path="./analytics_demo.json")
    
    # Add sample memories
    memory.add("User logged in", tags=["auth", "user"])
    memory.add("User updated profile", tags=["user", "profile"])
    memory.add("Error in payment", tags=["error", "payment"], priority="high")
    memory.add("Payment successful", tags=["payment", "success"])
    memory.add("User clicked button", tags=["ui", "interaction"])
    
    analytics = MemoryAnalytics(memory)
    
    print("=== Memory Analytics Demo ===\n")
    
    summary = analytics.get_summary()
    print("Summary:")
    print(f"  Total: {summary['total_memories']}")
    print(f"  Top Tags: {summary['top_tags']}")
    print(f"  Priorities: {summary['priority_distribution']}\n")
    
    timeline = analytics.get_timeline(days=7)
    print(f"Recent Timeline ({len(timeline)} items):")
    for item in timeline[:3]:
        print(f"  - {item['content'][:50]}...")
    
    cooccur = analytics.get_tag_cooccurrence()
    if cooccur:
        print(f"\nTag Co-occurrence: {cooccur}")
    
    # Cleanup
    import os
    os.remove("./analytics_demo.json")


if __name__ == "__main__":
    demo()
