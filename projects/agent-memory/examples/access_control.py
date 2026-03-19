"""
Memory Access Control
Control who can access what memories
"""
from agent_memory import Memory


class AccessControl:
    """Memory with access control"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.acls = {}  # mem_id -> set of allowed
    
    def grant(self, mem_id: str, user: str):
        """Grant access to user"""
        if mem_id not in self.acls:
            self.acls[mem_id] = set()
        self.acls[mem_id].add(user)
    
    def revoke(self, mem_id: str, user: str):
        """Revoke access"""
        if mem_id in self.acls:
            self.acls[mem_id].discard(user)
    
    def can_access(self, mem_id: str, user: str) -> bool:
        """Check if user can access"""
        # No ACL = public
        if mem_id not in self.acls:
            return True
        return user in self.acls[mem_id]
    
    def get_accessible(self, user: str) -> list:
        """Get memories accessible to user"""
        accessible = []
        
        for mem in self.memory.get_all():
            if self.can_access(mem.get("id"), user):
                accessible.append(mem)
        
        return accessible


class UserMemory:
    """Per-user memory isolation"""
    
    def __init__(self, base_memory: Memory, user: str):
        self.memory = base_memory
        self.user = user
        self.prefix = f"user:{user}:"
    
    def add(self, content: str, **kwargs):
        """Add with user prefix"""
        prefixed = f"{self.prefix}{content}"
        return self.memory.add(prefixed, **kwargs)
    
    def get_all(self):
        """Get user's memories"""
        all_mem = self.memory.get_all()
        return [m for m in all_mem if m.get("content", "").startswith(self.prefix)]


def demo():
    """Demo access control"""
    memory = Memory(storage="json", path="./acl_demo.json")
    acl = AccessControl(memory)
    
    print("=== Access Control Demo ===\n")
    
    # Add memories
    mem1_id = memory.add("Public memory", tags=["public"])
    mem2_id = memory.add("Private memory", tags=["private"])
    mem3_id = memory.add("Shared memory", tags=["shared"])
    
    # Grant access
    acl.grant(mem2_id, "alice")
    acl.grant(mem3_id, "alice")
    acl.grant(mem3_id, "bob")
    
    # Check access
    print(f"alice can access mem2: {acl.can_access(mem2_id, 'alice')}")
    print(f"bob can access mem2: {acl.can_access(mem2_id, 'bob')}")
    print(f"alice can access mem3: {acl.can_access(mem3_id, 'alice')}")
    print(f"bob can access mem3: {acl.can_access(mem3_id, 'bob')}")
    
    # User-specific memory
    alice_mem = UserMemory(memory, "alice")
    alice_mem.add("Alice's private note")
    
    print(f"\nAlice's memories: {len(alice_mem.get_all())}")
    
    # Cleanup
    import os
    if os.path.exists("./acl_demo.json"):
        os.remove("./acl_demo.json")


if __name__ == "__main__":
    demo()
