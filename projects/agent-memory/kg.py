#!/usr/bin/env python3
"""
Agent Memory v4.0 - Knowledge Graph Layer

Combines simple text memory with entity/relation knowledge graph.
Stores using Agent Memory backends but adds graph querying capabilities.
"""

import json
import uuid
from typing import List, Dict, Optional
from datetime import datetime

class KnowledgeGraph:
    """Knowledge graph layer on top of Agent Memory."""
    
    def __init__(self, memory_backend):
        """Initialize with an Agent Memory backend."""
        self.memory = memory_backend
        self._ensure_schema()
    
    def _ensure_schema(self):
        """Ensure memory has the right fields for graph data."""
        # Check if we have graph-related memories
        # We use special tags to identify graph elements
        pass
    
    def add_entity(self, name: str, entity_type: str, observations: List[str] = None) -> str:
        """Add an entity to the knowledge graph."""
        observations = observations or []
        
        # Store as a memory with special tags
        text = f"ENTITY: {name} (type: {entity_type})"
        if observations:
            text += f" | observations: {', '.join(observations)}"
        
        tags = ["_entity", entity_type, name]
        memory_id = self.memory.add_with_tags(
            text=text,
            tags=tags,
            metadata={"entity_type": entity_type, "observations": observations}
        )
        
        # Also store in memory index
        return memory_id
    
    def add_relation(self, from_entity: str, to_entity: str, relation_type: str) -> str:
        """Add a relation between two entities."""
        text = f"RELATION: {from_entity} --[{relation_type}]--> {to_entity}"
        
        memory_id = self.memory.add_with_tags(
            text=text,
            tags=["_relation", relation_type],
            metadata={
                "from": from_entity,
                "to": to_entity,
                "relation_type": relation_type
            }
        )
        return memory_id
    
    def query(self, entity_name: str = None, entity_type: str = None, 
              relation_type: str = None, depth: int = 1) -> Dict:
        """Query the knowledge graph.
        
        Args:
            entity_name: Filter by entity name
            entity_type: Filter by entity type
            relation_type: Filter by relation type
            depth: How many hops to traverse (not implemented yet)
            
        Returns:
            Dict with 'entities' and 'relations' keys
        """
        results = {"entities": [], "relations": []}
        
        # Query entities
        if entity_name or entity_type:
            tags = []
            if entity_type:
                tags.append(entity_type)
            if entity_name:
                tags.append(entity_name)
            
            entities = self.memory.get_by_tag(tags[0]) if tags else []
            for e in entities:
                if "_entity" in e.get("tags", []):
                    if not entity_name or entity_name in e["text"]:
                        results["entities"].append(e)
        
        # Query relations
        if relation_type:
            relations = self.memory.get_by_tag(relation_type)
            for r in relations:
                if "_relation" in r.get("tags", []):
                    results["relations"].append(r)
        else:
            # Get all relations
            relations = self.memory.get_by_tag("_relation")
            results["relations"] = relations
        
        return results
    
    def get_entity(self, name: str) -> Optional[Dict]:
        """Get a specific entity by name."""
        entities = self.memory.get_by_tag(name)
        for e in entities:
            if "_entity" in e.get("tags", []):
                return e
        return None
    
    def get_neighbors(self, entity_name: str, relation_type: str = None) -> List[Dict]:
        """Get all entities connected to a given entity."""
        # Find all relations involving this entity
        all_relations = self.memory.get_by_tag("_relation")
        neighbors = []
        
        for r in all_relations:
            meta = r.get("metadata", {})
            from_e = meta.get("from", "")
            to_e = meta.get("to", "")
            
            # Check if this entity is involved
            if entity_name in [from_e, to_e]:
                # Filter by relation type if specified
                if relation_type and meta.get("relation_type") != relation_type:
                    continue
                
                # Get the other entity
                other_name = to_e if from_e == entity_name else from_e
                other = self.get_entity(other_name)
                if other:
                    neighbors.append({
                        "entity": other,
                        "relation": r
                    })
        
        return neighbors
    
    def find_path(self, from_entity: str, to_entity: str, max_depth: int = 3) -> List[Dict]:
        """Find path between two entities using BFS.
        
        Returns list of relations forming the path.
        """
        if from_entity == to_entity:
            return [{"path": [from_entity], "relations": []}]
        
        visited = {from_entity}
        queue = [(from_entity, [])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) >= max_depth:
                continue
            
            # Get neighbors
            neighbors = self.get_neighbors(current)
            for n in neighbors:
                neighbor_entity = n["entity"]
                # Extract name from text
                name = neighbor_entity["text"].split("ENTITY: ")[1].split(" (type:")[0] if "ENTITY:" in neighbor_entity["text"] else ""
                
                if name == to_entity:
                    # Found!
                    full_path = path + [{"from": current, "to": name, "relation": n["relation"].get("metadata", {}).get("relation_type")}]
                    return [{"path": [from_entity] + [n["relation"].get("metadata", {}).get("to", name) for n in [n]], "relations": full_path}]
                
                if name not in visited:
                    visited.add(name)
                    new_path = path + [{"from": current, "to": name, "relation": n["relation"].get("metadata", {}).get("relation_type")}]
                    queue.append((name, new_path))
        
        return [{"path": [], "relations": [], "error": "No path found"}]
    
    def export_graph(self) -> Dict:
        """Export the entire graph as JSON."""
        entities = [e for e in self.memory.get_by_tag("_entity")]
        relations = [r for r in self.memory.get_by_tag("_relation")]
        
        # Build nodes and edges
        nodes = []
        seen_entities = set()
        
        for e in entities:
            meta = e.get("metadata", {})
            name = e["text"].split("ENTITY: ")[1].split(" (type:")[0] if "ENTITY:" in e["text"] else "unknown"
            if name not in seen_entities:
                nodes.append({
                    "id": name,
                    "type": meta.get("entity_type", "unknown"),
                    "observations": meta.get("observations", [])
                })
                seen_entities.add(name)
        
        edges = []
        for r in relations:
            meta = r.get("metadata", {})
            edges.append({
                "from": meta.get("from"),
                "to": meta.get("to"),
                "type": meta.get("relation_type")
            })
        
        return {"nodes": nodes, "edges": edges}


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from agent_memory import Memory
    
    # Create memory and graph
    memory = Memory(storage="json", path="./kg_demo.json")
    kg = KnowledgeGraph(memory)
    
    # Add some entities
    print("Adding entities...")
    kg.add_entity("Alice", "person", ["likes coding", "prefers dark mode"])
    kg.add_entity("Bob", "person", ["works at startup"])
    kg.add_entity("AgentMemory", "project", ["Python library", "MCP compatible"])
    
    # Add relations
    print("Adding relations...")
    kg.add_relation("Alice", "Bob", "colleague")
    kg.add_relation("Alice", "AgentMemory", "maintains")
    kg.add_relation("Bob", "AgentMemory", "uses")
    
    # Query
    print("\nQuery for 'person' type:")
    result = kg.query(entity_type="person")
    print(f"  Found {len(result['entities'])} entities")
    
    print("\nAlice's neighbors:")
    neighbors = kg.get_neighbors("Alice")
    for n in neighbors:
        print(f"  - {n['entity']['text'][:50]}...")
    
    print("\nExport graph:")
    graph = kg.export_graph()
    print(f"  Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")
    print(json.dumps(graph, indent=2))