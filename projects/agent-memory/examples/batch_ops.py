"""
Memory Batch Operations
Efficiently process multiple memories
"""
from agent_memory import Memory
from typing import List, Callable


class BatchProcessor:
    """Batch process memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def process(self, items: List[dict], operation: Callable) -> List[dict]:
        """Process items in batch"""
        results = []
        
        for item in items:
            try:
                result = operation(item)
                results.append({"success": True, "result": result})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
        
        return results
    
    def bulk_add(self, items: List[dict]) -> int:
        """Bulk add memories
        
        items: [{"content": "...", "tags": [...], "metadata": {...}}, ...]
        """
        added = 0
        
        for item in items:
            try:
                self.memory.add(
                    content=item.get("content", ""),
                    tags=item.get("tags", []),
                    metadata=item.get("metadata", {}),
                    priority=item.get("priority")
                )
                added += 1
            except Exception as e:
                print(f"Error adding: {e}")
        
        return added
    
    def bulk_delete(self, mem_ids: List[str]) -> int:
        """Bulk delete memories"""
        deleted = 0
        
        for mem_id in mem_ids:
            try:
                self.memory.forget(mem_id)
                deleted += 1
            except:
                pass
        
        return deleted
    
    def bulk_tag(self, mem_ids: List[str], tags: List[str]) -> int:
        """Bulk add tags"""
        updated = 0
        
        for mem_id in mem_ids:
            mem = self.memory.get(mem_id)
            if mem:
                current_tags = set(mem.get("tags", []))
                current_tags.update(tags)
                self.memory.update(mem_id, tags=list(current_tags))
                updated += 1
        
        return updated


class BulkImporter:
    """Import memories from various sources"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def from_lines(self, text: str, delimiter: str = "\n") -> int:
        """Import from line-separated text"""
        lines = [l.strip() for l in text.split(delimiter) if l.strip()]
        
        processor = BatchProcessor(self.memory)
        return processor.bulk_add([{"content": line} for line in lines])
    
    def from_json(self, data: List[dict]) -> int:
        """Import from JSON array"""
        processor = BatchProcessor(self.memory)
        return processor.bulk_add(data)


class BulkExporter:
    """Export memories in bulk"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_lines(self) -> str:
        """Export as line-separated text"""
        memories = self.memory.get_all()
        lines = [mem.get("content", "") for mem in memories]
        return "\n".join(lines)
    
    def to_json(self) -> List[dict]:
        """Export as JSON array"""
        return self.memory.get_all()


def demo():
    """Demo batch operations"""
    memory = Memory(storage="json", path="./batch_demo.json")
    processor = BatchProcessor(memory)
    
    print("=== Batch Processor Demo ===\n")
    
    # Bulk add
    items = [
        {"content": f"Memory {i}", "tags": ["batch"]}
        for i in range(10)
    ]
    
    added = processor.bulk_add(items)
    print(f"Bulk added: {added} memories")
    
    # Get all IDs
    all_memories = memory.get_all()
    ids = [m["id"] for m in all_memories[:5]]
    
    # Bulk tag
    tagged = processor.bulk_tag(ids, ["important"])
    print(f"Bulk tagged: {tagged} memories")
    
    # Bulk delete
    deleted = processor.bulk_delete(ids)
    print(f"Bulk deleted: {deleted} memories")
    
    # Remaining
    remaining = len(memory.get_all())
    print(f"Remaining: {remaining} memories")
    
    # Import demo
    importer = BulkImporter(memory)
    count = importer.from_lines("Line 1\nLine 2\nLine 3")
    print(f"Imported from lines: {count}")
    
    # Cleanup
    import os
    if os.path.exists("./batch_demo.json"):
        os.remove("./batch_demo.json")


if __name__ == "__main__":
    demo()
