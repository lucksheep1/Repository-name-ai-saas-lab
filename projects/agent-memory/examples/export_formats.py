"""
Memory Export Formats
Export to various formats
"""
from agent_memory import Memory


class ExportFormats:
    """Export to various formats"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_csv(self) -> str:
        """Export to CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["id", "content", "tags", "created_at"])
        
        for mem in self.memory.get_all():
            writer.writerow([
                mem.get("id", ""),
                mem.get("content", ""),
                ",".join(mem.get("tags", [])),
                mem.get("created_at", "")
            ])
        
        return output.getvalue()
    
    def to_markdown_table(self) -> str:
        """Export to Markdown table"""
        lines = ["| ID | Content | Tags |", "|---|---|---|"]
        
        for mem in self.memory.get_all()[:50]:
            content = mem.get("content", "")[:50].replace("|", "\\|")
            tags = ", ".join(mem.get("tags", []))
            
            lines.append(f"| {mem.get('id', '')[:8]} | {content} | {tags} |")
        
        return "\n".join(lines)
    
    def to_xml(self) -> str:
        """Export to XML"""
        lines = ['<?xml version="1.0"?>', "<memories>"]
        
        for mem in self.memory.get_all():
            lines.append("  <memory>")
            lines.append(f"    <id>{mem.get('id', '')}</id>")
            lines.append(f"    <content>{mem.get('content', '')}</content>")
            lines.append(f"    <tags>{','.join(mem.get('tags', []))}</tags>")
            lines.append("  </memory>")
        
        lines.append("</memories>")
        
        return "\n".join(lines)


def demo():
    """Demo export"""
    memory = Memory(storage="json", path="./export_demo2.json")
    
    memory.add("Test 1", tags=["a"])
    memory.add("Test 2", tags=["b"])
    
    exporter = ExportFormats(memory)
    
    print("=== Export Formats Demo ===\n")
    print("CSV:")
    print(exporter.to_csv()[:200])
    
    print("\nMarkdown:")
    print(exporter.to_markdown_table())
    
    import os
    if os.path.exists("./export_demo2.json"):
        os.remove("./export_demo2.json")


if __name__ == "__main__":
    demo()
