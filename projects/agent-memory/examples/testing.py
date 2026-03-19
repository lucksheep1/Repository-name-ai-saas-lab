"""
Memory Testing Utilities
Testing helpers for memory
"""
from agent_memory import Memory
import time


class MemoryFaker:
    """Generate fake test data"""
    
    @staticmethod
    def random_content() -> str:
        """Generate random memory content"""
        import random
        templates = [
            "User {action} {object}",
            "Meeting about {topic}",
            "Bug found in {component}",
            "Feature request: {feature}",
            "Note: {note}",
        ]
        
        actions = ["clicked", "submitted", "updated", "deleted", "created"]
        objects = ["button", "form", "page", "settings", "profile"]
        topics = ["project", "sprint", "release", "planning", "review"]
        components = ["login", "dashboard", "API", "database", "UI"]
        features = ["dark mode", "export", "import", "search", "filter"]
        notes = ["remember this", "important", "follow up", "check later", "review"]
        
        template = random.choice(templates)
        
        if "{action}" in template:
            template = template.replace("{action}", random.choice(actions))
        if "{object}" in template:
            template = template.replace("{object}", random.choice(objects))
        if "{topic}" in template:
            template = template.replace("{topic}", random.choice(topics))
        if "{component}" in template:
            template = template.replace("{component}", random.choice(components))
        if "{feature}" in template:
            template = template.replace("{feature}", random.choice(features))
        if "{note}" in template:
            template = template.replace("{note}", random.choice(notes))
        
        return template
    
    @staticmethod
    def fake_memories(memory: Memory, count: int = 10):
        """Generate fake memories"""
        for _ in range(count):
            content = MemoryFaker.random_content()
            tags = []
            
            if "bug" in content.lower():
                tags.append("bug")
            if "feature" in content.lower():
                tags.append("feature")
            if "meeting" in content.lower():
                tags.append("meeting")
            
            memory.add(content, tags=tags)


class MemoryTester:
    """Test memory functionality"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.passed = 0
        self.failed = 0
    
    def test_add(self) -> bool:
        """Test add functionality"""
        try:
            mem_id = self.memory.add("Test memory")
            assert mem_id is not None
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            print(f"test_add failed: {e}")
            return False
    
    def test_search(self) -> bool:
        """Test search functionality"""
        try:
            self.memory.add("Unique test content 12345")
            results = self.memory.search("12345")
            assert len(results) > 0
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            print(f"test_search failed: {e}")
            return False
    
    def test_tags(self) -> bool:
        """Test tags functionality"""
        try:
            mem_id = self.memory.add("Tagged memory", tags=["test"])
            mem = self.memory.get(mem_id)
            assert "test" in mem.get("tags", [])
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            print(f"test_tags failed: {e}")
            return False
    
    def test_priority(self) -> bool:
        """Test priority functionality"""
        try:
            mem_id = self.memory.add("Priority memory", metadata={"priority": 5})
            mem = self.memory.get(mem_id)
            assert mem.get("metadata", {}).get("priority") == 5
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            print(f"test_priority failed: {e}")
            return False
    
    def run_all(self) -> dict:
        """Run all tests"""
        self.test_add()
        self.test_search()
        self.test_tags()
        self.test_priority()
        
        return {
            "passed": self.passed,
            "failed": self.failed,
            "total": self.passed + self.failed
        }


def demo():
    """Demo testing utilities"""
    memory = Memory(storage="json", path="./test_demo.json")
    
    print("=== Memory Testing Demo ===\n")
    
    # Generate fake data
    print("Generating fake memories...")
    MemoryFaker.fake_memories(memory, count=5)
    print(f"Created {len(memory.get_all())} fake memories\n")
    
    # Run tests
    tester = MemoryTester(memory)
    results = tester.run_all()
    
    print(f"Test Results:")
    print(f"  Passed: {results['passed']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Total: {results['total']}")
    
    # Cleanup
    import os
    if os.path.exists("./test_demo.json"):
        os.remove("./test_demo.json")


if __name__ == "__main__":
    demo()
