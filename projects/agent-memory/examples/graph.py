"""
Memory Graph
Visualize memory relationships
"""
from agent_memory import Memory


class MemoryGraph:
    """Memory with relationship graph"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def link(self, from_id: str, to_id: str, rel: str):
        """Link two memories"""
        from_mem = self.memory.get(from_id)
        to_mem = self.memory.get(to_id)
        
        if from_mem and to_mem:
            # Store relationship in metadata
            links = from_mem.get("metadata", {}).get("_links", [])
            links.append({"to": to_id, "rel": rel})
            self.memory.update(from_id, metadata={**from_mem.get("metadata", {}), "_links": links})
    
    def get_links(self, mem_id: str) -> list:
        """Get memory links"""
        mem = self.memory.get(mem_id)
        if mem:
            return mem.get("metadata", {}).get("_links", [])
        return []
    
    def related(self, mem_id: str) -> list:
        """Get related memories"""
        links = self.get_links(mem_id)
        related = []
        
        for link in links:
            rel_mem = self.memory.get(link["to"])
            if rel_mem:
                related.append({**rel_mem, "relationship": link["rel"]})
        
        return related
    
    def to_graphviz(self) -> str:
        """Generate Graphviz DOT"""
        lines = ["digraph MemoryGraph {"]
        
        for mem in self.memory.get_all():
            mem_id = mem.get("id", "")
            content = mem.get("content", "")[:30].replace('"', '\\"')
            
            lines.append(f'  "{mem_id}" [label="{content}..."];')
            
            for link in mem.get("metadata", {}).get("_links", []):
                lines.append(f'  "{mem_id}" -> "{link["to"]}" [label="{link["rel"]}"];')
        
        lines.append("}")
        return "\n".join(lines)


def demo():
    """Demo graph"""
    memory = Memory(storage="json", path="./graph_demo.json")
    graph = MemoryGraph(memory)
    
    print("=== Memory Graph Demo ===\n")
    
    # Create memories
    id1 = memory.add("Project started")
    id2 = memory.add("Feature A implemented")
    id3 = memory.add("Bug fixed")
    id4 = memory.add("Released v1.0")
    
    # Link them
    graph.link(id1, id2, "implements")
    graph.link(id2, id3, "fixes")
    graph.link(id3, id4, "results_in")
    
    print(f"Links from memory 1: {graph.get_links(id1)}")
    
    # Related
    related = graph.related(id2)
    print(f"\nRelated to memory 2:")
    for r in related:
        print(f"  {r.get('relationship')}: {r.get('content')[:30]}")
    
    # Graphviz
    print("\nGraphviz DOT:")
    print(graph.to_graphviz()[:200])
    
    # Cleanup
    import os
    if os.path.exists("./graph_demo.json"):
        os.remove("./graph_demo.json")


if __name__ == "__main__":
    demo()
