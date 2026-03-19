"""
Memory Auto-Summary
Automatically summarize memories
"""
from agent_memory import Memory


class AutoSummary:
    """Auto-summarize memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def summarize_all(self, max_length: int = 100) -> str:
        """Summarize all memories"""
        memories = self.memory.get_all()
        
        if not memories:
            return "No memories to summarize."
        
        # Simple summarization (first sentence of recent memories)
        recent = memories[-5:]
        
        summary_parts = ["Summary of recent memories:"]
        
        for mem in recent:
            content = mem.get("content", "")
            
            # Take first sentence
            sentences = content.split(".")
            first = sentences[0].strip()
            
            if first:
                summary_parts.append(f"- {first}")
        
        return "\n".join(summary_parts)
    
    def summarize_by_tag(self, tag: str) -> str:
        """Summarize memories by tag"""
        mems = self.memory.get_by_tag(tag)
        
        if not mems:
            return f"No memories with tag '{tag}'."
        
        return f"Found {len(mems)} memories with tag '{tag}':\n" + \
            "\n".join(f"- {m.get('content', '')[:60]}" for m in mems[:5])
    
    def extract_topics(self) -> dict:
        """Extract topics from memories"""
        topics = {}
        
        for mem in self.memory.get_all():
            content = mem.get("content", "").lower()
            
            # Simple keyword extraction
            words = content.split()
            
            for word in words:
                if len(word) > 4:
                    topics[word] = topics.get(word, 0) + 1
        
        # Return top topics
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_topics[:20])


def demo():
    """Demo auto-summary"""
    memory = Memory(storage="json", path="./summary_demo.json")
    summarizer = AutoSummary(memory)
    
    print("=== Auto Summary Demo ===\n")
    
    # Add memories
    memory.add("Python is a great programming language for AI and machine learning.")
    memory.add("FastAPI is a modern web framework for building APIs.")
    memory.add("SQLite is a lightweight database that works great for small projects.")
    memory.add("Memory is important for AI agents to maintain context.")
    
    # Summarize
    print(summarizer.summarize_all())
    
    # Topics
    print("\nTop topics:")
    for topic, count in summarizer.extract_topics().items():
        print(f"  {topic}: {count}")
    
    # Cleanup
    import os
    if os.path.exists("./summary_demo.json"):
        os.remove("./summary_demo.json")


if __name__ == "__main__":
    demo()
