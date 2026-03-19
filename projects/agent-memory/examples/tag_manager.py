"""
Memory Tag Manager
Advanced tag management
"""
from agent_memory import Memory
from collections import defaultdict


class TagManager:
    """Manage tags"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_all_tags(self) -> dict:
        """Get all tags with counts"""
        tag_counts = defaultdict(int)
        
        for mem in self.memory.get_all():
            for tag in mem.get("tags", []):
                tag_counts[tag] += 1
        
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))
    
    def merge_tags(self, source: str, target: str) -> int:
        """Merge one tag into another"""
        merged = 0
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            
            if source in tags:
                tags.remove(source)
                
                if target not in tags:
                    tags.append(target)
                
                self.memory.update(mem["id"], tags=tags)
                merged += 1
        
        return merged
    
    def delete_tag(self, tag: str) -> int:
        """Delete a tag from all memories"""
        deleted = 0
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            
            if tag in tags:
                tags.remove(tag)
                self.memory.update(mem["id"], tags=tags)
                deleted += 1
        
        return deleted
    
    def rename_tag(self, old: str, new: str) -> int:
        """Rename a tag"""
        renamed = 0
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            
            if old in tags:
                tags.remove(old)
                tags.append(new)
                self.memory.update(mem["id"], tags=tags)
                renamed += 1
        
        return renamed
    
    def get_tag_cooccurrence(self) -> dict:
        """Find which tags appear together"""
        cooccur = defaultdict(int)
        
        for mem in self.memory.get_all():
            tags = mem.get("tags", [])
            
            if len(tags) > 1:
                for i, t1 in enumerate(tags):
                    for t2 in tags[i+1:]:
                        pair = tuple(sorted([t1, t2]))
                        cooccur[pair] += 1
        
        return dict(sorted(cooccur.items(), key=lambda x: x[1], reverse=True)[:10])


def demo():
    """Demo tag manager"""
    memory = Memory(storage="json", path="./tag_manager_demo.json")
    manager = TagManager(memory)
    
    print("=== Tag Manager Demo ===\n")
    
    # Add with tags
    memory.add("Python tutorial", tags=["python", "tutorial", "beginner"])
    memory.add("JS tutorial", tags=["javascript", "tutorial", "beginner"])
    memory.add("Python advanced", tags=["python", "advanced"])
    memory.add("React guide", tags=["javascript", "frontend"])
    
    # Show all tags
    print("All tags:")
    for tag, count in manager.get_all_tags().items():
        print(f"  {tag}: {count}")
    
    # Merge
    merged = manager.merge_tags("beginner", "easy")
    print(f"\nMerged 'beginner' into 'easy': {merged} memories")
    
    # Co-occurrence
    print("\nTag co-occurrence:")
    for pair, count in manager.get_tag_cooccurrence().items():
        print(f"  {pair[0]} + {pair[1]}: {count}")
    
    # Cleanup
    import os
    if os.path.exists("./tag_manager_demo.json"):
        os.remove("./tag_manager_demo.json")


if __name__ == "__main__":
    demo()
