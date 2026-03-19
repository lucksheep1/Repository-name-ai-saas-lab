"""
Session Manager Example
Manages multiple conversation sessions with isolated memories
"""
from agent_memory import Memory
import json
from datetime import datetime


class SessionManager:
    """Manages multiple agent memory sessions"""
    
    def __init__(self, storage="sqlite", base_path="./sessions"):
        self.storage = storage
        self.base_path = base_path
        self.sessions = {}  # session_id -> Memory instance
    
    def create_session(self, session_id: str, ttl_days: int = 7) -> Memory:
        """Create a new session with isolated memory"""
        path = f"{self.base_path}/session_{session_id}.db"
        memory = Memory(
            storage=self.storage,
            path=path,
            ttl_days=ttl_days
        )
        self.sessions[session_id] = memory
        return memory
    
    def get_session(self, session_id: str, ttl_days: int = 7) -> Memory:
        """Get or create a session"""
        if session_id not in self.sessions:
            return self.create_session(session_id, ttl_days)
        return self.sessions[session_id]
    
    def end_session(self, session_id: str):
        """Clean up a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def list_sessions(self):
        """List all active sessions"""
        return list(self.sessions.keys())
    
    def get_session_info(self, session_id: str) -> dict:
        """Get session metadata"""
        memory = self.get_session(session_id)
        memories = memory.get_all()
        
        return {
            "session_id": session_id,
            "memory_count": len(memories),
            "oldest": memories[0]["created_at"] if memories else None,
            "newest": memories[-1]["created_at"] if memories else None,
        }


def demo():
    """Demo session management"""
    manager = SessionManager(storage="json", base_path="./session_demo")
    
    # Create sessions for different users/conversations
    sessions = ["user_alice", "user_bob", "support_ticket_123"]
    
    for sid in sessions:
        mem = manager.get_session(sid)
        mem.add(f"Session {sid} started")
    
    # Add context to specific sessions
    alice_mem = manager.get_session("user_alice")
    alice_mem.add("Alice prefers email notifications")
    alice_mem.add("Alice is interested in premium features")
    
    bob_mem = manager.get_session("user_bob")
    bob_mem.add("Bob asked about pricing")
    bob_mem.add("Bob prefers SMS notifications")
    
    ticket_mem = manager.get_session("support_ticket_123")
    ticket_mem.add("Customer reported login issue")
    ticket_mem.add("Issue resolved: password reset sent")
    
    # Query specific session
    print("=== Session Manager Demo ===\n")
    print(f"Active sessions: {manager.list_sessions()}\n")
    
    for sid in sessions:
        info = manager.get_session_info(sid)
        print(f"Session: {sid}")
        print(f"  Memories: {info['memory_count']}")
        
        mem = manager.get_session(sid)
        recent = mem.search("prefers")  # Simple search
        if recent:
            print(f"  Key info: {recent[0]['content']}")
        print()
    
    # Cleanup demo files
    import os
    for f in os.listdir("./session_demo"):
        if f.endswith(".json"):
            os.remove(f"./session_demo/{f}")


if __name__ == "__main__":
    demo()
