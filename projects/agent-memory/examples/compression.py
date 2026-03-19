"""
Memory Compression
Compress old memories to save space
"""
from agent_memory import Memory
import zlib
import json
import base64


class CompressedMemory:
    """Memory with automatic compression"""
    
    def __init__(self, memory: Memory, compress_older_than_days: int = 7):
        self.memory = memory
        self.compress_older_than_days = compress_older_than_days
    
    def add(self, content: str, **kwargs):
        """Add memory (normal)"""
        return self.memory.add(content, **kwargs)
    
    def compress_all(self) -> int:
        """Compress old memories"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        compressed = 0
        
        for mem in self.memory.get_all():
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            age = (now - created).days
            
            if age >= self.compress_older_than_days:
                content = mem.get("content", "")
                
                # Compress
                compressed_content = self._compress(content)
                
                # Update with compressed
                self.memory.update(mem["id"], 
                    content=compressed_content,
                    metadata={**mem.get("metadata", {}), "_compressed": True}
                )
                compressed += 1
        
        return compressed
    
    def decompress(self, mem_id: str) -> str:
        """Decompress a memory"""
        mem = self.memory.get(mem_id)
        
        if not mem:
            return None
        
        if mem.get("metadata", {}).get("_compressed"):
            content = mem.get("content", "")
            return self._decompress(content)
        
        return mem.get("content", "")
    
    def _compress(self, content: str) -> str:
        """Compress string"""
        compressed = zlib.compress(content.encode())
        return base64.b64encode(compressed).decode()
    
    def _decompress(self, content: str) -> str:
        """Decompress string"""
        try:
            decoded = base64.b64decode(content.encode())
            return zlib.decompress(decoded).decode()
        except:
            return content


class SummarizedMemory:
    """Memory with auto-summarization"""
    
    def __init__(self, memory: Memory, summarize_older_than_days: int = 7):
        self.memory = memory
        self.summarize_older_than_days = summarize_older_than_days
    
    def summarize_all(self) -> int:
        """Summarize old memories"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        summarized = 0
        
        for mem in self.memory.get_all():
            created = datetime.fromisoformat(mem.get("created_at", now.isoformat()))
            age = (now - created).days
            
            if age >= self.summarize_older_than_days:
                content = mem.get("content", "")
                
                # Simple summarize (first 100 chars + note)
                summary = self._summarize(content)
                
                self.memory.update(mem["id"], 
                    content=summary,
                    metadata={**mem.get("metadata", {}), "_summarized": True}
                )
                summarized += 1
        
        return summarized
    
    def _summarize(self, content: str) -> str:
        """Summarize content"""
        max_len = 100
        
        if len(content) <= max_len:
            return content
        
        return content[:max_len] + f"... [was {len(content)} chars]"


def demo():
    """Demo compression"""
    memory = Memory(storage="json", path="./compress_demo.json")
    compressed = CompressedMemory(memory)
    
    print("=== Compressed Memory Demo ===\n")
    
    # Add memories
    compressed.add("Short memory")
    compressed.add("This is a much longer memory that contains a lot of " * 10)
    
    print("Added 2 memories")
    
    # Compress
    count = compressed.compress_all()
    print(f"Compressed {count} memories")
    
    # Show content (decompressed)
    for mem in memory.get_all():
        is_compressed = mem.get("metadata", {}).get("_compressed", False)
        content = compressed.decompress(mem["id"]) if is_compressed else mem.get("content", "")
        print(f"  [{'compressed' if is_compressed else 'normal'}] {content[:40]}...")
    
    # Cleanup
    import os
    if os.path.exists("./compress_demo.json"):
        os.remove("./compress_demo.json")


if __name__ == "__main__":
    demo()
