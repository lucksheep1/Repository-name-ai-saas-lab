"""
Memory Graph View
Visualize memories as a graph
"""
from agent_memory import Memory


class GraphBuilder:
    """Build graph from memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_dot(self) -> str:
        """Export to DOT format (Graphviz)"""
        lines = ["digraph memories {"]
        
        for mem in self.memory.get_all():
            mem_id = mem.get("id", "").replace("-", "_")[:8]
            content = mem.get("content", "").replace('"', '\\"')[:30]
            tags = mem.get("tags", [])
            
            color = "white"
            if "bug" in tags:
                color = "red"
            elif "feature" in tags:
                color = "green"
            
            lines.append(f'    {mem_id} [label="{content}..." color={color}]')
        
        lines.append("}")
        return "\n".join(lines)
    
    def to_mermaid(self) -> str:
        """Export to Mermaid format"""
        lines = ["graph TD;"]
        
        for mem in self.memory.get_all():
            mem_id = mem.get("id", "").replace("-", "")[:8]
            content = mem.get("content", "").replace("'", "")[:30]
            
            lines.append(f'    {mem_id}["{content}..."]')
        
        return "\n".join(lines)


def demo():
    memory = Memory(storage="json", path="./graph_demo.json")
    memory.add("Bug in login", tags=["bug"])
    memory.add("Feature: dark mode", tags=["feature"])
    memory.add("Note: check later")
    
    gb = GraphBuilder(memory)
    print("DOT format:")
    print(gb.to_dot())
    print("\nMermaid format:")
    print(gb.to_mermaid())
    
    import os
    if os.path.exists("./graph_demo.json"):
        os.remove("./graph_demo.json")


if __name__ == "__main__":
    demo()
