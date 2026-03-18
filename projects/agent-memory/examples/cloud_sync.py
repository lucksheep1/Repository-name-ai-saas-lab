#!/usr/bin/env python3
"""
Agent Memory - Sync to Cloud
============================
Sync memory to cloud storage (S3, GCS, etc.)

Usage:
    from cloud_sync import CloudSyncMemory
    
    memory = CloudSyncMemory(storage="json", path="./memory.json", sync_to_s3=True)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from typing import Optional
from agent_memory import Memory


class CloudSyncMemory(Memory):
    """Memory with cloud sync."""
    
    def __init__(self, *args, sync_enabled: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.sync_enabled = sync_enabled
        self.last_sync = None
    
    def sync_to_file(self, filepath: str):
        """Export and save to file (simulates cloud upload)."""
        self.export(filepath)
        self.last_sync = time.time()
        print(f"Synced to: {filepath}")
    
    def sync_from_file(self, filepath: str):
        """Import from file (simulates cloud download)."""
        self.import_(filepath)
        self.last_sync = time.time()
        print(f"Synced from: {filepath}")
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add and optionally sync."""
        result = super().add(text, metadata, ttl_days)
        if self.sync_enabled:
            # Auto-sync on add (simplified - in production use queue)
            pass
        return result
    
    def get_sync_status(self) -> dict:
        """Get sync status."""
        return {
            "enabled": self.sync_enabled,
            "last_sync": self.last_sync
        }


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "sync_demo.json")
    cloud_path = os.path.join(tempfile.gettempdir(), "cloud_backup.json")
    
    for p in [demo_path, cloud_path]:
        if os.path.exists(p):
            os.remove(p)
    
    print("🤖 Agent Memory - Cloud Sync Demo")
    print("=" * 50)
    
    # Create memory
    memory = CloudSyncMemory(storage="json", path=demo_path, sync_enabled=True)
    
    # Add memories
    print("\n1. Adding memories...")
    memory.add("Remember to sync")
    memory.add("Cloud backup important")
    memory.add("Don't forget")
    
    print(f"   Total: {memory.count()}")
    
    # Sync
    print("\n2. Syncing to cloud...")
    memory.sync_to_file(cloud_path)
    print(f"   Status: {memory.get_sync_status()}")
    
    # Clear and restore
    print("\n3. Clearing local memory...")
    memory.clear()
    print(f"   Total: {memory.count()}")
    
    # Restore
    print("\n4. Restoring from cloud...")
    memory.sync_from_file(cloud_path)
    print(f"   Total: {memory.count()}")
    
    print("\n✅ Demo complete!")
    
    # Cleanup
    for p in [demo_path, cloud_path]:
        if os.path.exists(p):
            os.remove(p)
