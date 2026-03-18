#!/usr/bin/env python3
"""
Agent Memory - Export Formats
=============================
Export memory to various formats (CSV, XML, HTML, etc.)

Usage:
    from export_formats import export_csv, export_xml, export_html
    
    export_csv(memory, "memory.csv")
    export_xml(memory, "memory.xml")
    export_html(memory, "memory.html")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import json
from typing import List, Dict
from agent_memory import Memory


def export_csv(memory: Memory, filepath: str):
    """Export memory to CSV."""
    memories = memory.get_recent(limit=memory.count())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'text', 'timestamp', 'tags', 'priority'])
        writer.writeheader()
        
        for mem in memories:
            writer.writerow({
                'id': mem.get('id', ''),
                'text': mem.get('text', ''),
                'timestamp': mem.get('timestamp', ''),
                'tags': ','.join(mem.get('tags', [])),
                'priority': mem.get('priority', 0)
            })
    
    print(f"Exported to CSV: {filepath}")


def export_xml(memory: Memory, filepath: str):
    """Export memory to XML."""
    memories = memory.get_recent(limit=memory.count())
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<memories>\n')
        
        for mem in memories:
            f.write('  <memory>\n')
            f.write(f'    <id>{mem.get("id", "")}</id>\n')
            
            # Escape XML special characters
            text = mem.get("text", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            f.write(f'    <text>{text}</text>\n')
            f.write(f'    <timestamp>{mem.get("timestamp", "")}</timestamp>\n')
            
            tags = mem.get("tags", [])
            for tag in tags:
                f.write(f'    <tag>{tag}</tag>\n')
            
            f.write(f'    <priority>{mem.get("priority", 0)}</priority>\n')
            f.write('  </memory>\n')
        
        f.write('</memories>\n')
    
    print(f"Exported to XML: {filepath}")


def export_html(memory: Memory, filepath: str):
    """Export memory to HTML."""
    memories = memory.get_recent(limit=memory.count())
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Agent Memory Export</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .memory { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 12px 0; }
        .tags { margin-top: 8px; }
        .tag { display: inline-block; background: #e0e0e0; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-right: 4px; }
        .timestamp { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <h1>🤖 Agent Memory Export</h1>
    <p>Total memories: ''' + str(len(memories)) + '''</p>
''')
        
        for mem in memories:
            f.write('    <div class="memory">\n')
            f.write(f'        <p>{mem.get("text", "")}</p>\n')
            f.write(f'        <p class="timestamp">{mem.get("timestamp", "")}</p>\n')
            
            tags = mem.get("tags", [])
            if tags:
                f.write('        <div class="tags">\n')
                for tag in tags:
                    f.write(f'            <span class="tag">{tag}</span>\n')
                f.write('        </div>\n')
            
            f.write('    </div>\n')
        
        f.write('''</body>
</html>''')
    
    print(f"Exported to HTML: {filepath}")


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "export_demo.json")
    csv_path = os.path.join(tempfile.gettempdir(), "export.csv")
    xml_path = os.path.join(tempfile.gettempdir(), "export.xml")
    html_path = os.path.join(tempfile.gettempdir(), "export.html")
    
    for p in [demo_path, csv_path, xml_path, html_path]:
        if os.path.exists(p):
            os.remove(p)
    
    print("🤖 Agent Memory - Export Formats Demo")
    print("=" * 50)
    
    # Create and populate memory
    memory = Memory(storage="json", path=demo_path)
    
    print("\n1. Adding memories...")
    memory.add_with_tags("Fix login bug", tags=["bug", "urgent"], metadata={"priority": 5})
    memory.add_with_tags("Add dark mode", tags=["feature", "ui"], metadata={"priority": 3})
    memory.add_with_tags("Write tests", tags=["testing"], metadata={"priority": 2})
    memory.add_with_tags("Update docs", tags=["docs"], metadata={"priority": 1})
    
    print(f"   Total: {memory.count()}")
    
    # Export to CSV
    print("\n2. Exporting to CSV...")
    export_csv(memory, csv_path)
    
    # Export to XML
    print("\n3. Exporting to XML...")
    export_xml(memory, xml_path)
    
    # Export to HTML
    print("\n4. Exporting to HTML...")
    export_html(memory, html_path)
    
    # Show files
    print("\n5. Generated files:")
    for p in [csv_path, xml_path, html_path]:
        if os.path.exists(p):
            size = os.path.getsize(p)
            print(f"   - {p} ({size} bytes)")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    for p in [demo_path, csv_path, xml_path, html_path]:
        if os.path.exists(p):
            os.remove(p)
