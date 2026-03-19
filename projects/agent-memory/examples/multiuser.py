"""
Memory Multi-User
Multi-user memory support
"""
from agent_memory import Memory


class UserMemory:
    """Isolated memory per user"""
    
    def __init__(self, memory: Memory, user_id: str):
        self.memory = memory
        self.user_id = user_id
        self.prefix = f"user:{user_id}:"
    
    def add(self, content: str, **kwargs):
        """Add user-specific memory"""
        return self.memory.add(
            f"{self.prefix}{content}",
            tags=["user", self.user_id] + kwargs.get("tags", []),
            metadata=kwargs.get("metadata", {})
        )
    
    def get_all(self):
        """Get user's memories"""
        return [m for m in self.memory.get_all() 
                if f"user:{self.user_id}:" in m.get("content", "")]
    
    def search(self, query: str):
        """Search user's memories"""
        return [m for m in self.memory.search(query) 
                if f"user:{self.user_id}:" in m.get("content", "")]


class TeamMemory:
    """Shared memory for teams"""
    
    def __init__(self, memory: Memory, team_id: str):
        self.memory = memory
        self.team_id = team_id
        self.prefix = f"team:{team_id}:"
    
    def add(self, content: str, user_id: str = None, **kwargs):
        """Add team memory"""
        meta = kwargs.get("metadata", {})
        meta["team"] = self.team_id
        meta["user"] = user_id
        
        return self.memory.add(
            f"{self.prefix}{content}",
            tags=["team", self.team_id] + kwargs.get("tags", []),
            metadata=meta
        )
    
    def get_all(self):
        """Get team memories"""
        return self.memory.get_by_tag(self.team_id)
    
    def get_by_user(self, user_id: str):
        """Get user's contributions to team"""
        team_mems = self.get_all()
        return [m for m in team_mems 
                if m.get("metadata", {}).get("user") == user_id]


def demo():
    """Demo multi-user"""
    memory = Memory(storage="json", path="./multiuser_demo.json")
    
    print("=== Multi-User Demo ===\n")
    
    # User memories
    alice = UserMemory(memory, "alice")
    bob = UserMemory(memory, "bob")
    
    alice.add("Alice's secret")
    alice.add("Alice's preference: dark mode")
    bob.add("Bob's note")
    
    print(f"Alice's memories: {len(alice.get_all())}")
    print(f"Bob's memories: {len(bob.get_all())}")
    
    # Team memory
    team = TeamMemory(memory, "engineering")
    team.add("Sprint planning", user_id="alice")
    team.add("Code review", user_id="bob")
    
    print(f"Team memories: {len(team.get_all())}")
    
    # Cleanup
    import os
    if os.path.exists("./multiuser_demo.json"):
        os.remove("./multiuser_demo.json")


if __name__ == "__main__":
    demo()
