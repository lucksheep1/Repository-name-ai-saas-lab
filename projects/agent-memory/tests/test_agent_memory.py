"""Tests for agent_memory."""
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_memory import Memory


def test_add_memory():
    """Test adding a memory."""
    memory = Memory(storage="json", path="./test_memory.json")
    memory.clear()
    
    memory_id = memory.add("Test memory")
    assert memory_id is not None
    assert memory.count() == 1
    
    memory.clear()
    os.remove("./test_memory.json")


def test_add_with_tags():
    """Test adding memory with tags."""
    memory = Memory(storage="json", path="./test_tags.json")
    memory.clear()
    
    memory.add_with_tags("Bug in code", tags=["bug", "urgent"])
    memory.add_with_tags("Feature request", tags=["feature"])
    
    bugs = memory.get_by_tag("bug")
    assert len(bugs) == 1
    
    features = memory.get_by_tag("feature")
    assert len(features) == 1
    
    memory.clear()
    os.remove("./test_tags.json")


def test_search():
    """Test memory search."""
    memory = Memory(storage="json", path="./test_search.json")
    memory.clear()
    
    memory.add("User prefers dark mode")
    memory.add("User likes blue color")
    memory.add("User is from China")
    
    results = memory.search("dark theme")
    assert len(results) > 0
    
    memory.clear()
    os.remove("./test_search.json")


def test_priority():
    """Test priority functionality."""
    memory = Memory(storage="json", path="./test_priority.json")
    memory.clear()
    
    memory.add("Low priority task", metadata={"priority": 1})
    memory.add("High priority issue", metadata={"priority": 5})
    
    high_priority = memory.get_by_priority(4)
    assert len(high_priority) == 1
    
    memory.clear()
    os.remove("./test_priority.json")


def test_export_import():
    """Test export and import."""
    memory = Memory(storage="json", path="./test_export.json")
    memory.clear()
    
    memory.add("Memory to export")
    memory.export("./test_backup.json")
    
    # Import to new memory
    memory2 = Memory(storage="json", path="./test_import.json")
    memory2.import_("./test_backup.json")
    
    assert memory2.count() == 1
    
    # Cleanup
    memory.clear()
    memory2.clear()
    os.remove("./test_export.json")
    os.remove("./test_import.json")
    os.remove("./test_backup.json")


def test_timeline():
    """Test timeline functionality."""
    memory = Memory(storage="json", path="./test_timeline.json")
    memory.clear()
    
    memory.add("First memory")
    memory.add("Second memory")
    
    timeline = memory.get_timeline()
    assert len(timeline) == 2
    
    memory.clear()
    os.remove("./test_timeline.json")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
