#!/usr/bin/env python3
"""
Agent Memory - Encrypted Memory
==============================
Encrypt sensitive memories.

Usage:
    from encrypted import EncryptedMemory
    
    memory = EncryptedMemory(secret_key="my-secret-key")
    memory.add("Sensitive data")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import hashlib
from typing import Optional
try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

from agent_memory import Memory


class EncryptedMemory(Memory):
    """Memory with encryption."""
    
    def __init__(self, *args, secret_key: str = "default", **kwargs):
        super().__init__(*args, **kwargs)
        
        if HAS_CRYPTO:
            # Generate key from secret
            key = hashlib.sha256(secret_key.encode()).digest()
            self.cipher = Fernet(base64.urlsafe_b64encode(key))
        else:
            self.cipher = None
    
    def _encrypt(self, text: str) -> str:
        """Encrypt text."""
        if not self.cipher:
            return text
        return self.cipher.encrypt(text.encode()).decode()
    
    def _decrypt(self, encrypted: str) -> str:
        """Decrypt text."""
        if not self.cipher:
            return encrypted
        try:
            return self.cipher.decrypt(encrypted.encode()).decode()
        except:
            return encrypted
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add encrypted memory."""
        encrypted_text = self._encrypt(text)
        return super().add(encrypted_text, metadata, ttl_days)
    
    def get_recent(self, limit: int = 10):
        """Get recent memories (decrypted)."""
        memories = super().get_recent(limit)
        
        # Decrypt
        for mem in memories:
            mem["text"] = self._decrypt(mem["text"])
        
        return memories
    
    def search(self, query: str, top_k: int = 5):
        """Search memories (limited - can't search encrypted)."""
        # Get all and decrypt for search
        all_memories = self.get_recent(limit=self.count())
        
        # Simple search on decrypted
        results = []
        for mem in all_memories:
            if query.lower() in mem["text"].lower():
                results.append(mem)
                if len(results) >= top_k:
                    break
        
        return results


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "encrypted_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Encrypted Demo")
    print("=" * 50)
    
    if not HAS_CRYPTO:
        print("⚠️ cryptography not installed. Running basic demo.")
    
    # Create encrypted memory
    memory = EncryptedMemory(storage="json", path=demo_path, secret_key="secret123")
    
    # Add memories
    print("\n1. Adding encrypted memories...")
    memory.add("API Key: sk-1234567890")
    memory.add("Password: mypassword123")
    memory.add("Public note: Hello world")
    
    print(f"   Total: {memory.count()}")
    
    # Get recent (decrypted)
    print("\n2. Getting recent (decrypted):")
    recent = memory.get_recent(limit=3)
    for mem in recent:
        print(f"   - {mem['text']}")
    
    # Search
    print("\n3. Searching for 'password':")
    results = memory.search("password")
    for mem in results:
        print(f"   - {mem['text']}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
