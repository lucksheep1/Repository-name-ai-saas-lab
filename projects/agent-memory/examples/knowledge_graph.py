"""
Memory Knowledge Graph
Entity extraction and relationships
"""
from agent_memory import Memory
import re


class EntityExtractor:
    """Extract entities from memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.entities = {}  # entity -> list of mem_ids
    
    def extract(self, text: str) -> dict:
        """Extract entities from text"""
        entities = {
            "emails": re.findall(r'[\w.-]+@[\w.-]+', text),
            "urls": re.findall(r'https?://[^\s]+', text),
            "mentions": re.findall(r'@(\w+)', text),
            "hashtags": re.findall(r'#(\w+)', text),
        }
        
        # Extract capitalized words as potential names
        names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
        entities["names"] = names
        
        return entities
    
    def index(self, mem_id: str):
        """Index memory entities"""
        mem = self.memory.get(mem_id)
        if not mem:
            return
        
        text = mem.get("content", "")
        entities = self.extract(text)
        
        # Store in metadata
        self.memory.update(mem_id, metadata={
            **mem.get("metadata", {}),
            "_entities": entities
        })
        
        # Add to index
        for etype, values in entities.items():
            for v in values:
                if v not in self.entities:
                    self.entities[v] = []
                self.entities[v].append(mem_id)
    
    def search_by_entity(self, entity: str) -> list:
        """Find memories with entity"""
        if entity in self.entities:
            return [self.memory.get(mid) for mid in self.entities[entity]]
        return []


def demo():
    """Demo entity extraction"""
    memory = Memory(storage="json", path="./entity_demo.json")
    extractor = EntityExtractor(memory)
    
    print("=== Entity Extraction Demo ===\n")
    
    # Add memories with entities
    memory.add("Contact @john at john@example.com for help")
    memory.add("Check https://api.example.com/docs for docs")
    memory.add("Meeting with @alice about #projectX")
    
    # Index
    for mem in memory.get_all():
        extractor.index(mem.get("id"))
    
    # Search
    print("Search for 'john':")
    for m in extractor.search_by_entity("john"):
        print(f"  {m.get('content')}")
    
    print("\nSearch for 'example.com':")
    for m in extractor.search_by_entity("example.com"):
        print(f"  {m.get('content')}")
    
    print("\nAll entities:", extractor.entities)
    
    # Cleanup
    import os
    if os.path.exists("./entity_demo.json"):
        os.remove("./entity_demo.json")


if __name__ == "__main__":
    demo()
