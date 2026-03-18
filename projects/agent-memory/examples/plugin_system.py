#!/usr/bin/env python3
"""
Agent Memory - Plugin System
============================
Extend memory with plugins.

Usage:
    from plugin_system import MemoryWithPlugins
    
    memory = MemoryWithPlugins()
    memory.register_plugin(TimestampPlugin())
    memory.register_plugin(KeywordExtractor())
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from typing import List, Dict, Any, Callable
from datetime import datetime
from agent_memory import Memory


class MemoryPlugin:
    """Base class for memory plugins."""
    
    def on_add(self, memory_id: str, text: str, metadata: dict) -> dict:
        """Called when memory is added. Return updated metadata."""
        return metadata
    
    def on_search(self, query: str, results: List[dict]) -> List[dict]:
        """Called after search. Return filtered/modified results."""
        return results


class TimestampPlugin(MemoryPlugin):
    """Add timestamp to metadata."""
    
    def on_add(self, memory_id: str, text: str, metadata: dict) -> dict:
        metadata = metadata or {}
        metadata["added_at"] = datetime.now().isoformat()
        return metadata


class KeywordExtractor(MemoryPlugin):
    """Extract keywords from text."""
    
    def on_add(self, memory_id: str, text: str, metadata: dict) -> dict:
        metadata = metadata or {}
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter common words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and', 'in', 'for', 'on', 'at'}
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        metadata["keywords"] = list(set(keywords))[:5]
        return metadata


class SentimentPlugin(MemoryPlugin):
    """Simple sentiment analysis."""
    
    def on_add(self, memory_id: str, text: str, metadata: dict) -> dict:
        metadata = metadata or {}
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'awesome', 'love', 'like', 'happy', 'excellent']
        negative_words = ['bad', 'hate', 'terrible', 'awful', 'sad', 'angry', 'problem']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            metadata["sentiment"] = "positive"
        elif neg_count > pos_count:
            metadata["sentiment"] = "negative"
        else:
            metadata["sentiment"] = "neutral"
        
        return metadata


class MemoryWithPlugins(Memory):
    """Memory with plugin support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins: List[MemoryPlugin] = []
    
    def register_plugin(self, plugin: MemoryPlugin):
        """Register a plugin."""
        self.plugins.append(plugin)
    
    def add(self, text: str, metadata: dict = None, ttl_days: int = None) -> str:
        """Add memory with plugin processing."""
        # Run through plugins
        for plugin in self.plugins:
            metadata = plugin.on_add("", text, metadata)
        
        # Add memory
        memory_id = super().add(text, metadata, ttl_days)
        
        # Update metadata with ID
        for plugin in self.plugins:
            metadata = plugin.on_add(memory_id, text, metadata)
        
        return memory_id
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search with plugin post-processing."""
        results = super().search(query, top_k)
        
        # Run through plugins
        for plugin in self.plugins:
            results = plugin.on_search(query, results)
        
        return results


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "plugin_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Plugin System Demo")
    print("=" * 50)
    
    # Create memory with plugins
    memory = MemoryWithPlugins(storage="json", path=demo_path)
    memory.register_plugin(TimestampPlugin())
    memory.register_plugin(KeywordExtractor())
    memory.register_plugin(SentimentPlugin())
    
    # Add memories
    print("\n1. Adding memories with plugins...")
    memory.add("I love this great product!", metadata={"source": "user"})
    memory.add("There is a bad bug in the system", metadata={"source": "user"})
    memory.add("Working on a new Python project", metadata={"source": "user"})
    
    # Get recent with metadata
    print("\n2. Recent memories with metadata:")
    recent = memory.get_recent(limit=3)
    for mem in recent:
        print(f"   Text: {mem['text']}")
        print(f"   Keywords: {mem.get('metadata', {}).get('keywords', [])}")
        print(f"   Sentiment: {mem.get('metadata', {}).get('sentiment', 'N/A')}")
        print()
    
    print("✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
