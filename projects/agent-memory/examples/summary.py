"""
Memory Summarization
Auto-summarize memories
"""
from agent_memory import Memory


class MemorySummarizer:
    """Summarize memories"""
    
    def summarize(self, content: str, max_len: int = 100) -> str:
        """Summarize content"""
        if len(content) <= max_len:
            return content
        
        # Simple: take first sentence + key points
        sentences = content.split(".")
        
        if len(sentences) > 1:
            summary = sentences[0] + "."
            
            # Add more if needed
            if len(summary) < max_len // 2:
                for s in sentences[1:]:
                    if len(summary) + len(s) < max_len:
                        summary += s + "."
            
            return summary
        
        return content[:max_len] + "..."
    
    def summarize_all(self, memory: Memory) -> dict:
        """Summarize all memories"""
        summaries = []
        
        for mem in memory.get_all():
            content = mem.get("content", "")
            summary = self.summarize(content)
            
            summaries.append({
                "id": mem.get("id"),
                "original": content[:50] + "...",
                "summary": summary
            })
        
        return summaries


class ConversationSummary:
    """Summarize conversation"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def summarize_conversation(self) -> str:
        """Summarize entire conversation"""
        messages = self.memory.get_all()
        
        if not messages:
            return "No conversation yet."
        
        # Get topics
        topics = set()
        for m in messages:
            tags = m.get("tags", [])
            topics.update(tags)
        
        # Count message types
        roles = {}
        for m in messages:
            role = m.get("metadata", {}).get("role", "unknown")
            roles[role] = roles.get(role, 0) + 1
        
        summary = f"Conversation with {len(messages)} messages.\n"
        summary += f"Topics: {', '.join(topics) if topics else 'general'}\n"
        summary += f"Messages by role: {roles}"
        
        return summary


def demo():
    """Demo summarization"""
    memory = Memory(storage="json", path="./summary_demo.json")
    
    print("=== Memory Summarization Demo ===\n")
    
    # Add memories
    memory.add("This is a very long memory that contains a lot of detailed information about various topics including programming, science, and mathematics. It has many sentences and paragraphs.")
    memory.add("Short.")
    
    # Summarize
    summarizer = MemorySummarizer()
    for s in summarizer.summarize_all(memory):
        print(f"Original: {s['original']}")
        print(f"Summary: {s['summary']}\n")
    
    # Conversation summary
    conv = ConversationSummary(memory)
    memory.add("User message 1", metadata={"role": "user"})
    memory.add("Assistant response", metadata={"role": "assistant"})
    
    print("Conversation:", conv.summarize_conversation())
    
    # Cleanup
    import os
    if os.path.exists("./summary_demo.json"):
        os.remove("./summary_demo.json")


if __name__ == "__main__":
    demo()
