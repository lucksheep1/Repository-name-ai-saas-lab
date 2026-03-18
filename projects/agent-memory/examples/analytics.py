#!/usr/bin/env python3
"""
Agent Memory - Memory Analytics
===============================
Analytics and insights from memory data.

Usage:
    from analytics import MemoryAnalytics
    
    analytics = MemoryAnalytics(memory)
    stats = analytics.get_stats()
    patterns = analytics.find_patterns()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from collections import Counter
from agent_memory import Memory


class MemoryAnalytics:
    """Analytics for memory data."""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_stats(self) -> Dict[str, Any]:
        """Get basic statistics."""
        recent = self.memory.get_recent(limit=min(100, self.memory.count()))
        
        # Count tags
        all_tags = []
        for mem in recent:
            all_tags.extend(mem.get("tags", []))
        tag_counts = Counter(all_tags)
        
        # Count priorities
        priorities = [m.get("priority", 0) for m in recent]
        priority_counts = Counter(priorities)
        
        return {
            "total_memories": self.memory.count(),
            "unique_tags": len(tag_counts),
            "top_tags": tag_counts.most_common(5),
            "priority_distribution": dict(priority_counts),
            "avg_priority": sum(priorities) / len(priorities) if priorities else 0
        }
    
    def find_patterns(self) -> Dict[str, Any]:
        """Find patterns in memory data."""
        recent = self.memory.get_recent(limit=min(100, self.memory.count()))
        
        # Find common words
        all_words = []
        for mem in recent:
            words = mem["text"].lower().split()
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        
        # Find time-based patterns
        timestamps = []
        for mem in recent:
            ts = mem.get("timestamp", "")
            if ts:
                timestamps.append(ts[:10])  # Just the date
        
        date_counts = Counter(timestamps)
        
        return {
            "common_words": word_counts.most_common(10),
            "activity_by_date": dict(date_counts.most_common(5))
        }
    
    def get_insights(self) -> List[str]:
        """Generate insights from memory."""
        insights = []
        
        stats = self.get_stats()
        
        # High priority count
        high_priority = sum(1 for p in stats["priority_distribution"].keys() if p >= 4)
        if high_priority > 0:
            insights.append(f"You have {high_priority} high-priority items")
        
        # Tag insights
        if stats["top_tags"]:
            top_tag = stats["top_tags"][0]
            insights.append(f"Most used tag: '{top_tag[0]}' ({top_tag[1]} times)")
        
        # Word patterns
        patterns = self.find_patterns()
        if patterns["common_words"]:
            top_word = patterns["common_words"][0]
            if top_word[1] > 1:
                insights.append(f"Common word: '{top_word[0]}' ({top_word[1]} times)")
        
        return insights


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "analytics_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Analytics Demo")
    print("=" * 50)
    
    memory = Memory(storage="json", path=demo_path)
    
    # Add some memories
    print("\n1. Adding memories...")
    memory.add_with_tags("Fix bug in login", tags=["bug", "urgent"], metadata={"priority": 5})
    memory.add_with_tags("Add dark mode", tags=["feature", "ui"], metadata={"priority": 3})
    memory.add_with_tags("Update tests", tags=["testing"], metadata={"priority": 2})
    memory.add_with_tags("Fix another bug", tags=["bug"], metadata={"priority": 4})
    memory.add_with_tags("Add dark mode to settings", tags=["feature", "ui"], metadata={"priority": 2})
    memory.add_with_tags("Write documentation", tags=["docs"], metadata={"priority": 1})
    memory.add_with_tags("Fix critical crash", tags=["bug", "urgent"], metadata={"priority": 5})
    
    # Analytics
    analytics = MemoryAnalytics(memory)
    
    print("\n2. Statistics:")
    stats = analytics.get_stats()
    print(f"   Total memories: {stats['total_memories']}")
    print(f"   Unique tags: {stats['unique_tags']}")
    print(f"   Top tags: {stats['top_tags']}")
    print(f"   Priority distribution: {stats['priority_distribution']}")
    
    print("\n3. Patterns:")
    patterns = analytics.find_patterns()
    print(f"   Common words: {patterns['common_words'][:5]}")
    print(f"   Activity by date: {patterns['activity_by_date']}")
    
    print("\n4. Insights:")
    insights = analytics.get_insights()
    for insight in insights:
        print(f"   💡 {insight}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
