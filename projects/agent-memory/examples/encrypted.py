"""
Memory Encryption
Secure memory storage with encryption
"""
from agent_memory import Memory
from cryptography.fernet import Fernet
import base64
import hashlib
import json


class EncryptedMemory:
    """Memory with automatic encryption"""
    
    def __init__(self, memory: Memory, password: str):
        self.memory = memory
        self.cipher = self._create_cipher(password)
    
    def _create_cipher(self, password: str):
        """Create cipher from password"""
        # Derive key from password
        key = hashlib.sha256(password.encode()).digest()
        key_b64 = base64.urlsafe_b64encode(key)
        return Fernet(key_b64)
    
    def add(self, content: str, **kwargs):
        """Add encrypted memory"""
        # Encrypt content
        encrypted = self.cipher.encrypt(content.encode()).decode()
        return self.memory.add(encrypted, **kwargs)
    
    def get(self, mem_id: str):
        """Get and decrypt memory"""
        mem = self.memory.get(mem_id)
        if mem:
            try:
                mem["content"] = self.cipher.decrypt(
                    mem["content"].encode()
                ).decode()
            except:
                pass  # Not encrypted (legacy)
        return mem
    
    def get_all(self):
        """Get all decrypted memories"""
        memories = []
        for mem in self.memory.get_all():
            try:
                mem["content"] = self.cipher.decrypt(
                    mem["content"].encode()
                ).decode()
            except:
                pass  # Not encrypted
            memories.append(mem)
        return memories
    
    def search(self, query: str, **kwargs):
        """Search (returns encrypted - can't search encrypted)"""
        # Warning: search won't work on encrypted content
        print("⚠️ Warning: Search doesn't work on encrypted content!")
        return []


def demo():
    """Demo encryption"""
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("cryptography not installed, skipping demo")
        return
    
    password = "secret_password"
    
    memory = Memory(storage="json", path="./encrypted_demo.json")
    encrypted = EncryptedMemory(memory, password)
    
    print("=== Encrypted Memory Demo ===\n")
    
    # Add encrypted memories
    encrypted.add("Secret information 1")
    encrypted.add("Secret information 2", tags=["private"])
    
    print("Added 2 encrypted memories")
    
    # Retrieve (decrypted)
    all_mem = encrypted.get_all()
    print(f"\nRetrieved {len(all_mem)} decrypted memories:")
    for mem in all_mem:
        print(f"  - {mem['content']}")
    
    # Cleanup
    import os
    if os.path.exists("./encrypted_demo.json"):
        os.remove("./encrypted_demo.json")


if __name__ == "__main__":
    demo()
