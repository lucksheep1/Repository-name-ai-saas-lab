"""
Memory Data Export/Import Formats
Export/import in various data formats
"""
from agent_memory import Memory
import json
import csv
import xml.etree.ElementTree as ET


class MultiFormatExporter:
    """Export to multiple formats"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def to_json(self, filepath: str) -> int:
        """Export to JSON"""
        data = self.memory.get_all()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return len(data)
    
    def to_csv(self, filepath: str) -> int:
        """Export to CSV"""
        data = self.memory.get_all()
        if not data:
            return 0
        
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "content", "tags", "created_at", "priority"])
            for mem in data:
                writer.writerow([
                    mem.get("id", ""),
                    mem.get("content", ""),
                    "|".join(mem.get("tags", [])),
                    mem.get("created_at", ""),
                    mem.get("metadata", {}).get("priority", "")
                ])
        return len(data)
    
    def to_xml(self, filepath: str) -> int:
        """Export to XML"""
        data = self.memory.get_all()
        root = ET.Element("memories")
        
        for mem in data:
            m = ET.SubElement(root, "memory")
            ET.SubElement(m, "id").text = str(mem.get("id", ""))
            ET.SubElement(m, "content").text = mem.get("content", "")
            ET.SubElement(m, "tags").text = ",".join(mem.get("tags", []))
            ET.SubElement(m, "created_at").text = mem.get("created_at", "")
        
        ET.ElementTree(root).write(filepath, encoding="utf-8")
        return len(data)


def demo():
    memory = Memory(storage="json", path="./format_demo.json")
    memory.add("Test 1", tags=["a"])
    memory.add("Test 2", tags=["b"])
    
    exporter = MultiFormatExporter(memory)
    
    print("Exported to JSON:", exporter.to_json("out.json"))
    print("Exported to CSV:", exporter.to_csv("out.csv"))
    print("Exported to XML:", exporter.to_xml("out.xml"))
    
    import os
    for f in ["out.json", "out.csv", "out.xml", "./format_demo.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
