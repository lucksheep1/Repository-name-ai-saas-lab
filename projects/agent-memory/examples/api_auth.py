"""
Memory API Authentication
Secure API with authentication
"""
from agent_memory import Memory
import hashlib
import hmac
import time


class AuthMemory:
    """Memory with API authentication"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.api_keys = {}  # key -> {"user": ..., "created": ...}
    
    def create_key(self, user: str) -> str:
        """Create API key for user"""
        import random
        import string
        
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        self.api_keys[key] = {
            "user": user,
            "created": time.time()
        }
        
        return key
    
    def verify_key(self, key: str) -> str:
        """Verify API key, return user or None"""
        if key in self.api_keys:
            return self.api_keys[key]["user"]
        return None
    
    def revoke_key(self, key: str):
        """Revoke API key"""
        if key in self.api_keys:
            del self.api_keys[key]


class SecureMemory:
    """Memory with signed requests"""
    
    def __init__(self, memory: Memory, secret: str):
        self.memory = memory
        self.secret = secret
    
    def sign(self, data: str) -> str:
        """Sign data"""
        return hmac.new(
            self.secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify(self, data: str, signature: str) -> bool:
        """Verify signature"""
        return hmac.compare_digest(self.sign(data), signature)
    
    def add_signed(self, content: str, signature: str, **kwargs) -> str:
        """Add with signature verification"""
        if not self.verify(content, signature):
            raise ValueError("Invalid signature")
        
        return self.memory.add(content, **kwargs)


def demo():
    """Demo auth"""
    memory = Memory(storage="json", path="./auth_demo.json")
    auth = AuthMemory(memory)
    secure = SecureMemory(memory, "my_secret_key")
    
    print("=== Auth Memory Demo ===\n")
    
    # Create API key
    key = auth.create_key("alice")
    print(f"Created key for alice: {key[:10]}...")
    
    # Verify
    user = auth.verify_key(key)
    print(f"Verified: {user}")
    
    # Bad key
    user = auth.verify_key("invalid_key")
    print(f"Bad key: {user}")
    
    # Signed request
    content = "Important memory"
    signature = secure.sign(content)
    
    mem_id = secure.add_signed(content, signature)
    print(f"\nAdded signed memory: {mem_id}")
    
    # Cleanup
    import os
    if os.path.exists("./auth_demo.json"):
        os.remove("./auth_demo.json")


if __name__ == "__main__":
    demo()
