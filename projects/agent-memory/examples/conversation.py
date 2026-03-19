"""
Memory Conversation Context
Build context from conversation history
"""
from agent_memory import Memory


class ConversationContext:
    """Build context from conversations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def build(self, max_tokens: int = 2000, include_system: bool = True) -> str:
        """Build context string"""
        parts = []
        
        if include_system:
            parts.append("## Conversation Context\n")
        
        memories = self.memory.get_all()
        
        for mem in memories:
            content = mem.get("content", "")
            role = mem.get("metadata", {}).get("role", "user")
            
            # Format based on role
            if role == "system":
                parts.append(f"System: {content}")
            elif role == "assistant":
                parts.append(f"Assistant: {content}")
            else:
                parts.append(f"User: {content}")
        
        # Truncate to token limit (rough estimate)
        context = "\n".join(parts)
        
        if len(context) > max_tokens * 4:  # Rough: 4 chars/token
            context = context[-max_tokens * 4:]
        
        return context
    
    def add_message(self, content: str, role: str = "user"):
        """Add message to conversation"""
        self.memory.add(content, metadata={"role": role})
    
    def get_recent(self, count: int = 10) -> list:
        """Get recent messages"""
        all_mem = self.memory.get_all()
        return all_mem[-count:]


class PersonaMemory:
    """Memory with persona configuration"""
    
    def __init__(self, memory: Memory, persona: dict):
        self.memory = memory
        self.persona = persona
    
    def get_context_prompt(self) -> str:
        """Get context prompt for LLM"""
        parts = [
            "## Persona",
            f"Name: {self.persona.get('name', 'AI')}",
            f"Description: {self.persona.get('description', '')}",
            "",
            "## Knowledge",
        ]
        
        # Add memories as knowledge
        for mem in self.memory.get_all():
            parts.append(f"- {mem.get('content', '')}")
        
        return "\n".join(parts)


def demo():
    """Demo conversation context"""
    memory = Memory(storage="json", path="./conv_demo.json")
    ctx = ConversationContext(memory)
    
    print("=== Conversation Context Demo ===\n")
    
    # Add conversation
    ctx.add_message("Hello, I'm John", "user")
    ctx.add_message("Hi John! How can I help?", "assistant")
    ctx.add_message("I need help with Python", "user")
    ctx.add_message("Sure, what specifically?", "assistant")
    ctx.add_message("How do I use lists?", "user")
    
    # Build context
    context = ctx.build()
    print("Context:\n")
    print(context)
    
    print("\n--- Recent ---")
    for m in ctx.get_recent(3):
        role = m.get("metadata", {}).get("role", "user")
        print(f"{role}: {m.get('content')}")
    
    # Cleanup
    import os
    if os.path.exists("./conv_demo.json"):
        os.remove("./conv_demo.json")


if __name__ == "__main__":
    demo()
