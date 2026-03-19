"""
Memory Export/Import Utilities
Export memories to various formats and import from backups
"""
from agent_memory import Memory
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


class MemoryExporter:
    """Export memories to various formats"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_json(self, filepath: str = "export.json") -> int:
        """Export to JSON format"""
        memories = self.memory.get_all()
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        
        return len(memories)
    
    def to_csv(self, filepath: str = "export.csv") -> int:
        """Export to CSV format"""
        memories = self.memory.get_all()
        
        if not memories:
            return 0
        
        # Get all possible fields
        fields = ["id", "content", "created_at", "updated_at", "tags", "priority", "metadata"]
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            
            for mem in memories:
                # Convert complex fields to strings
                row = mem.copy()
                if "tags" in row:
                    row["tags"] = "|".join(row["tags"]) if row["tags"] else ""
                if "metadata" in row:
                    row["metadata"] = json.dumps(row["metadata"])
                writer.writerow(row)
        
        return len(memories)
    
    def to_markdown(self, filepath: str = "export.md") -> int:
        """Export to Markdown format"""
        memories = self.memory.get_all()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Memory Export\n\n")
            f.write(f"Exported: {datetime.now().isoformat()}\n\n")
            f.write(f"Total: {len(memories)} memories\n\n---\n\n")
            
            for i, mem in enumerate(memories, 1):
                f.write(f"## {i}. {mem.get('created_at', 'Unknown date')}\n\n")
                f.write(f"{mem.get('content', '')}\n\n")
                
                if mem.get("tags"):
                    f.write(f"**Tags:** {', '.join(mem['tags'])}\n\n")
                
                if mem.get("priority"):
                    f.write(f"**Priority:** {mem['priority']}\n\n")
                
                f.write("---\n\n")
        
        return len(memories)
    
    def to_xml(self, filepath: str = "export.xml") -> int:
        """Export to XML format"""
        memories = self.memory.get_all()
        
        root = ET.Element("memories")
        root.set("count", str(len(memories)))
        root.set("exported", datetime.now().isoformat())
        
        for mem in memories:
            mem_elem = ET.SubElement(root, "memory")
            mem_elem.set("id", str(mem.get("id", "")))
            
            content = ET.SubElement(mem_elem, "content")
            content.text = mem.get("content", "")
            
            created = ET.SubElement(mem_elem, "created_at")
            created.text = mem.get("created_at", "")
            
            if mem.get("tags"):
                tags = ET.SubElement(mem_elem, "tags")
                for tag in mem["tags"]:
                    tag_elem = ET.SubElement(tags, "tag")
                    tag_elem.text = tag
            
            if mem.get("priority"):
                priority = ET.SubElement(mem_elem, "priority")
                priority.text = mem["priority"]
        
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        
        return len(memories)


class MemoryImporter:
    """Import memories from various formats"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def from_json(self, filepath: str) -> int:
        """Import from JSON"""
        with open(filepath, "r", encoding="utf-8") as f:
            memories = json.load(f)
        
        imported = 0
        for mem in memories:
            self.memory.add(
                content=mem.get("content", ""),
                tags=mem.get("tags", []),
                metadata=mem.get("metadata", {}),
                priority=mem.get("priority")
            )
            imported += 1
        
        return imported
    
    def from_csv(self, filepath: str) -> int:
        """Import from CSV"""
        imported = 0
        
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                tags = row.get("tags", "").split("|") if row.get("tags") else []
                tags = [t.strip() for t in tags if t.strip()]
                
                metadata = {}
                if row.get("metadata"):
                    try:
                        metadata = json.loads(row["metadata"])
                    except:
                        pass
                
                self.memory.add(
                    content=row.get("content", ""),
                    tags=tags,
                    metadata=metadata,
                    priority=row.get("priority") or None
                )
                imported += 1
        
        return imported


def demo():
    """Demo export/import"""
    # Create sample memory
    memory = Memory(storage="json", path="./export_demo.json")
    
    memory.add("Sample memory 1", tags=["demo", "test"])
    memory.add("Sample memory 2", tags=["demo", "example"], priority="high")
    memory.add("Sample memory 3", tags=["test"])
    
    exporter = MemoryExporter(memory)
    importer = MemoryImporter(memory)
    
    print("=== Export/Import Demo ===\n")
    
    # Export to various formats
    counts = {
        "json": exporter.to_json("./demo_export.json"),
        "csv": exporter.to_csv("./demo_export.csv"),
        "md": exporter.to_markdown("./demo_export.md"),
    }
    
    print(f"Exported {counts['json']} memories to each format")
    print("Files: demo_export.json, demo_export.csv, demo_export.md")
    
    # Show JSON export
    print("\nJSON Preview:")
    with open("./demo_export.json", "r") as f:
        data = json.load(f)
        print(json.dumps(data[:2], indent=2)[:500])
    
    # Cleanup
    import os
    for f in ["./export_demo.json", "./demo_export.json", 
              "./demo_export.csv", "./demo_export.md"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
