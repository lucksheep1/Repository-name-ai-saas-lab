"""
Memory Knowledge Graph
Build knowledge graph from memories
"""
from agent_memory import Memory
from collections import defaultdict


class KnowledgeGraph:
    """Build graph from memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.entities = defaultdict(set)  # entity -> related
        self.relations = defaultdict(list)  # (e1, e2) -> relation
    
    def build(self):
        """Build graph from memories"""
        # Clear
        self.entities.clear()
        self.relations.clear()
        
        for mem in self.memory.get_all():
            content = mem.get("content", "")
            
            # Simple entity extraction (capitalized words)
            import re
            entities = re.findall(r'\b[A-Z][a-z]+\b', content)
            
            for entity in entities:
                self.entities[entity].add(mem["id"])
            
            # Simple relations (co-occurrence)
            for i, e1 in enumerate(entities):
                for e2 in entities[i+1:]:
                    key = tuple(sorted([e1, e2]))
                    self.relations[key].append(mem["id"])
    
    def get_related(self, entity: str) -> list:
        """Get entities related to this one"""
        related_ids = self.entities.get(entity, set())
        
        related = []
        for mem in self.memory.get_all():
            if mem["id"] in related_ids:
                related.append(mem)
        
        return related
    
    def get_relations(self, entity1: str, entity2: str) -> list:
        """Get relation between two entities"""
        key = tuple(sorted([entity1, entity2]))
        mem_ids = self.relations.get(key, [])
        
        return [self.memory.get(mid) for mid in mem_ids if self.memory.get(mid)]


class ConceptMemory:
    """Memory organized by concepts"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.concepts = defaultdict(list)  # concept -> memories
    
    def index(self):
        """Index memories by concepts"""
        self.concepts.clear()
        
        for mem in self.memory.get_all():
            content = mem.get("content", "").lower()
            
            # Simple concept detection
            concept_keywords = {
                "code": ["code", "function", "class", "method"],
                "data": ["data", "database", "query", "storage"],
                "user": ["user", "login", "profile", "account"],
                "api": ["api", "endpoint", "request", "response"],
                "error": ["error", "bug", "issue", "problem"],
            }
            
            for concept, keywords in concept_keywords.items():
                if any(kw in content for kw in keywords):
                    self.concepts[concept].append(mem["id"])
    
    def get_concept(self, concept: str) -> list:
        """Get memories by concept"""
        mem_ids = self.concepts.get(concept, [])
        return [self.memory.get(mid) for mid in mem_ids if self.memory.get(mid)]


def demo():
    """Demo knowledge graph"""
    memory = Memory(storage="json", path="./graph_demo.json")
    
    # Add memories with entities
    memory.add("Python is great for AI")
    memory.add("Python has great libraries")
    memory.add("AI uses machine learning")
    memory.add("Machine learning needs data")
    
    print("=== Knowledge Graph Demo ===\n")
    
    # Build graph
    kg = KnowledgeGraph(memory)
    kg.build()
    
    print(f"Entities: {list(kg.entities.keys())}")
    print(f"Relations: {len(kg.relations)} pairs")
    
    # Query
    print("\nRelated to 'Python':")
    for mem in kg.get_related("Python"):
        print(f"  {mem.get('content')}")
    
    # Concept memory
    cm = ConceptMemory(memory)
    cm.index()
    
    print(f"\nConcepts: {list(cm.concepts.keys())}")
    
    # Cleanup
    import os
    if os.path.exists("./graph_demo.json"):
        os.remove("./graph_demo.json")


if __name__ == "__main__":
    demo()
