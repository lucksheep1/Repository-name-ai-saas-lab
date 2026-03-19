"""
Memory Q&A System
Q&A based on memory
"""
from agent_memory import Memory


class QASystem:
    """Q&A from memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def ask(self, question: str) -> str:
        """Answer question from memory"""
        # Find relevant memories
        results = self.memory.search(question)
        
        if not results:
            return "I don't have information about that."
        
        # Build answer
        answer = "Based on my memory:\n\n"
        
        for r in results[:3]:
            answer += f"- {r.get('content')}\n"
        
        return answer
    
    def train(self, q: str, a: str):
        """Train Q&A pair"""
        self.memory.add(f"Q: {q} A: {a}", tags=["qa"])


def demo():
    """Demo Q&A"""
    memory = Memory(storage="json", path="./qa_demo.json")
    qa = QASystem(memory)
    
    # Train
    qa.train("What is Python?", "Python is a programming language")
    qa.train("What is AI?", "AI is artificial intelligence")
    
    # Ask
    print("=== Q&A Demo ===\n")
    print(qa.ask("Python"))
    print("\n", qa.ask("AI"))
    
    import os
    if os.path.exists("./qa_demo.json"):
        os.remove("./qa_demo.json")


if __name__ == "__main__":
    demo()
