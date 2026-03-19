"""
Memory Validation & Sanitization
Validate and sanitize memory content
"""
from agent_memory import Memory
import re
from typing import List, Optional


class MemoryValidator:
    """Validate and sanitize memory content"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.rules = []
    
    def add_rule(self, name: str, validate: callable, fix: callable = None):
        """Add validation rule"""
        self.rules.append({
            "name": name,
            "validate": validate,
            "fix": fix
        })
    
    def validate(self, content: str) -> dict:
        """Validate content against all rules"""
        issues = []
        
        for rule in self.rules:
            if not rule["validate"](content):
                issues.append(rule["name"])
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def sanitize(self, content: str) -> str:
        """Sanitize content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Remove potential SQL injection
        dangerous = ["DROP ", "DELETE ", "INSERT ", "UPDATE ", "CREATE "]
        for word in dangerous:
            if word in content.upper():
                content = content.replace(word, "")
        
        # Limit length
        max_length = 10000
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        return content
    
    def add_with_validation(self, content: str, **kwargs) -> str:
        """Add with validation and sanitization"""
        # Sanitize first
        content = self.sanitize(content)
        
        # Validate
        result = self.validate(content)
        
        if not result["valid"]:
            print(f"⚠️ Validation issues: {result['issues']}")
        
        return self.memory.add(content, **kwargs)


# Default rules
def no_html(content: str) -> bool:
    """Check for HTML tags"""
    return not bool(re.search(r'<[^>]+>', content))


def no_urls(content: str) -> bool:
    """Check for URLs (optional)"""
    url_pattern = r'https?://[^\s]+'
    return not bool(re.search(url_pattern, content))


def reasonable_length(content: str) -> bool:
    """Check length is reasonable"""
    return 1 <= len(content) <= 10000


def no_special_chars(content: str) -> bool:
    """Check for special characters (optional)"""
    # Allow common punctuation
    allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?-_\'"')
    return all(c in allowed or ord(c) < 128 for c in content)


def demo():
    """Demo validation"""
    memory = Memory(storage="json", path="./validator_demo.json")
    validator = MemoryValidator(memory)
    
    # Add rules
    validator.add_rule("no_html", no_html)
    validator.add_rule("reasonable_length", reasonable_length)
    
    print("=== Memory Validator Demo ===\n")
    
    # Valid content
    valid = "Hello, this is a valid memory!"
    mem_id = validator.add_with_validation(valid)
    print(f"✓ Added valid: {mem_id}")
    
    # Content with issues (will be sanitized)
    dirty = "  Multiple   spaces   and  <script>alert('xss')</script>"
    mem_id = validator.add_with_validation(dirty)
    print(f"✓ Added sanitized: {mem_id}")
    
    # Show result
    all_mem = memory.get_all()
    print(f"\nTotal memories: {len(all_mem)}")
    
    # Cleanup
    import os
    if os.path.exists("./validator_demo.json"):
        os.remove("./validator_demo.json")


if __name__ == "__main__":
    demo()
