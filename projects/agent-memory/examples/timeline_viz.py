"""
Memory Timeline Visualization
Visualize memory as a timeline
"""
from agent_memory import Memory
from datetime import datetime, timedelta


class TimelineVisualizer:
    """Create timeline visualizations"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_text(self, max_items: int = 20) -> str:
        """Create text-based timeline"""
        memories = self.memory.get_timeline(limit=max_items)
        
        if not memories:
            return "No memories yet."
        
        lines = ["📜 Memory Timeline", "=" * 40, ""]
        
        for mem in memories:
            created = mem.get("created_at", "")
            content = mem.get("content", "")[:60]
            
            # Add tags
            tags = mem.get("tags", [])
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            
            lines.append(f"• {created[:16]} | {content}...{tag_str}")
        
        return "\n".join(lines)
    
    def to_html(self, max_items: int = 50) -> str:
        """Create HTML timeline"""
        memories = self.memory.get_timeline(limit=max_items)
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }
        .timeline { border-left: 3px solid #ddd; padding-left: 20px; margin-left: 10px; }
        .memory { margin-bottom: 20px; position: relative; }
        .memory::before { content: '•'; position: absolute; left: -26px; color: #666; font-size: 24px; }
        .date { color: #888; font-size: 12px; }
        .content { margin: 5px 0; }
        .tags { display: flex; gap: 5px; }
        .tag { background: #e0e0e0; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
    </style>
</head>
<body>
    <h1>🕐 Memory Timeline</h1>
    <div class="timeline">
"""
        
        for mem in memories:
            created = mem.get("created_at", "Unknown")
            content = mem.get("content", "")
            tags = mem.get("tags", [])
            
            tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
            
            html += f"""
        <div class="memory">
            <div class="date">{created}</div>
            <div class="content">{content}</div>
            <div class="tags">{tags_html}</div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def to_markdown(self, max_items: int = 30) -> str:
        """Create markdown timeline"""
        memories = self.memory.get_timeline(limit=max_items)
        
        md = ["# Memory Timeline", "", "---", ""]
        
        for mem in memories:
            created = mem.get("created_at", "")
            content = mem.get("content", "")
            tags = mem.get("tags", [])
            
            tag_str = f" **Tags:** {', '.join(tags)}" if tags else ""
            
            md.append(f"## {created[:16]}")
            md.append(f"{content}{tag_str}")
            md.append("")
        
        return "\n".join(md)


def demo():
    """Demo timeline"""
    memory = Memory(storage="json", path="./timeline_demo.json")
    
    # Add memories with different times
    memory.add("Started project", tags=["init"])
    memory.add("Added feature X", tags=["feature"])
    memory.add("Fixed bug", tags=["bug", "urgent"])
    memory.add("User feedback received", tags=["feedback"])
    
    viz = TimelineVisualizer(memory)
    
    print("=== Timeline Visualizer Demo ===\n")
    
    print("Text Timeline:")
    print(viz.to_text())
    
    print("\n" + "="*40)
    print("\nMarkdown Timeline:")
    print(viz.to_markdown())
    
    # Save HTML
    html = viz.to_html()
    with open("./timeline_demo.html", "w") as f:
        f.write(html)
    print(f"\nSaved HTML timeline to: ./timeline_demo.html")
    
    # Cleanup
    import os
    for f in ["./timeline_demo.json", "./timeline_demo.html"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
