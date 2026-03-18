#!/usr/bin/env python3
"""
Agent Memory - Compression
===========================
Compress old memories to save space.

Usage:
    from compression import CompressedMemory
    
    memory = CompressedMemory()
    # Old memories get compressed automatically
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import zlib
import base64
from typing import List, Dict, Any
from agent_memory import Memory


class CompressedMemory(Memory):
    """Memory with automatic compression of old memories."""
    
    def __init__(self, *args, compression_threshold_days: int = 7, **kwargs):
        super().__init__(*args, **kwargs)
        self.compression_threshold_days = compression_threshold_days
    
    def compress_memory(self, memory_id: str) -> bool:
        """Compress a specific memory."""
        recent = self.get_recent(limit=self.count())
        
        for mem in recent:
            if mem["id"] == memory_id:
                text = mem["text"]
                
                # Compress
                compressed = zlib.compress(text.encode())
                encoded = base64.b64encode(compressed).decode()
                
                # Replace with compressed version
                self.delete(memory_id)
                self.add(f"[COMPRESSED]{encoded}", metadata={
                    "compressed": True,
                    "original_length": len(text)
                })
                return True
        
        return False
    
    def decompress_memory(self, memory_id: str) -> str:
        """Decompress a memory."""
        recent = self.get_recent(limit=self.count())
        
        for mem in recent:
            if mem["id"] == memory_id:
                text = mem["text"]
                if text.startswith("[COMPRESSED]"):
                    encoded = text[12:]
                    compressed = base64.b64decode(encoded)
                    decompressed = zlib.decompress(compressed).decode()
                    return decompressed
                return text
        
        return ""
    
    def auto_compress_old(self, days: int = 7):
        """Compress memories older than specified days."""
        # This is a simplified version
        # In production, you'd check timestamps
        recent = self.get_recent(limit=self.count())
        
        # Compress half of them for demo
        to_compress = recent[len(recent)//2:]
        
        for mem in to_compress:
            if not mem.get("metadata", {}).get("compressed"):
                self.compress_memory(mem["id"])


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "compression_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Compression Demo")
    print("=" * 50)
    
    memory = CompressedMemory(storage="json", path=demo_path)
    
    # Add some long memories
    print("\n1. Adding long memories...")
    long_text1 = "This is a very long memory " * 50
    long_text2 = "Another long memory " * 50
    
    id1 = memory.add(long_text1)
    id2 = memory.add(long_text2)
    
    print(f"   Memory 1 length: {len(long_text1)}")
    print(f"   Memory 2 length: {len(long_text2)}")
    
    # Get sizes
    recent = memory.get_recent(limit=2)
    for mem in recent:
        print(f"   Stored length: {len(mem['text'])}")
    
    # Compress
    print("\n2. Compressing memories...")
    memory.compress_memory(id1)
    
    recent = memory.get_recent(limit=2)
    for mem in recent:
        is_compressed = mem["text"].startswith("[COMPRESSED]")
        print(f"   Compressed: {is_compressed}, Length: {len(mem['text'])}")
    
    # Decompress
    print("\n3. Decompressing...")
    decompressed = memory.decompress_memory(id1)
    print(f"   Original restored: {len(decompressed)} chars")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
