#!/usr/bin/env python3
"""
Agent Memory - Backup Manager
=============================
Automated backup and restore.

Usage:
    from backup_manager import BackupManager
    
    manager = BackupManager(memory)
    manager.backup()  # Create backup
    manager.restore(backup_id)  # Restore from backup
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from typing import List, Dict, Optional
from datetime import datetime
from agent_memory import Memory


class BackupManager:
    """Manage memory backups."""
    
    def __init__(self, memory: Memory, backup_dir: str = "./backups"):
        self.memory = memory
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup(self, name: str = None) -> str:
        """Create a backup."""
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get all memories
        memories = self.memory.get_recent(limit=self.memory.count())
        
        # Create backup
        backup = {
            "name": name,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "count": len(memories),
            "memories": memories
        }
        
        # Save
        filepath = os.path.join(self.backup_dir, f"backup_{name}.json")
        with open(filepath, "w") as f:
            json.dump(backup, f, indent=2, default=str)
        
        return filepath
    
    def restore(self, backup_path: str) -> int:
        """Restore from backup."""
        with open(backup_path, "r") as f:
            backup = json.load(f)
        
        # Clear current memory
        self.memory.clear()
        
        # Restore memories
        restored = 0
        for mem in backup.get("memories", []):
            text = mem.get("text", "")
            tags = mem.get("tags", [])
            metadata = mem.get("metadata", {})
            
            if tags:
                self.memory.add_with_tags(text, tags=tags, metadata=metadata)
            else:
                self.memory.add(text, metadata=metadata)
            
            restored += 1
        
        return restored
    
    def list_backups(self) -> List[Dict]:
        """List all backups."""
        backups = []
        
        for filename in os.listdir(self.backup_dir):
            if filename.startswith("backup_") and filename.endswith(".json"):
                filepath = os.path.join(self.backup_dir, filename)
                with open(filepath, "r") as f:
                    data = json.load(f)
                    backups.append({
                        "name": data.get("name"),
                        "datetime": data.get("datetime"),
                        "count": data.get("count"),
                        "path": filepath
                    })
        
        # Sort by datetime (newest first)
        backups.sort(key=lambda x: x.get("datetime", ""), reverse=True)
        
        return backups
    
    def delete_backup(self, backup_path: str) -> bool:
        """Delete a backup."""
        try:
            os.remove(backup_path)
            return True
        except:
            return False
    
    def auto_backup(self, interval_hours: int = 24) -> str:
        """Create timestamped backup."""
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.backup(name)


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "backup_demo.json")
    backup_dir = os.path.join(tempfile.gettempdir(), "backups")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
    
    print("🤖 Agent Memory - Backup Manager Demo")
    print("=" * 50)
    
    # Create memory with data
    memory = Memory(storage="json", path=demo_path)
    
    print("\n1. Adding memories...")
    memory.add("Memory 1")
    memory.add("Memory 2")
    memory.add("Memory 3")
    print(f"   Total: {memory.count()}")
    
    # Create backup manager
    manager = BackupManager(memory, backup_dir)
    
    print("\n2. Creating backup...")
    backup_path = manager.backup("test_backup")
    print(f"   Saved to: {backup_path}")
    
    print("\n3. Adding more memories...")
    memory.add("Memory 4")
    memory.add("Memory 5")
    print(f"   Total: {memory.count()}")
    
    print("\n4. Restoring from backup...")
    restored = manager.restore(backup_path)
    print(f"   Restored: {restored} memories")
    print(f"   Current: {memory.count()} memories")
    
    print("\n5. Listing backups...")
    backups = manager.list_backups()
    for b in backups:
        print(f"   - {b['datetime']}: {b['count']} memories")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    if os.path.exists(demo_path):
        os.remove(demo_path)
    if os.path.exists(backup_dir):
        import shutil
        shutil.rmtree(backup_dir)
