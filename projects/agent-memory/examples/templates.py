"""
Memory Templates
Pre-defined memory patterns
"""
from agent_memory import Memory
from typing import Dict, List


class MemoryTemplate:
    """Template for common memory patterns"""
    
    def __init__(self, name: str, fields: Dict[str, str]):
        self.name = name
        self.fields = fields  # field_name -> description
    
    def render(self, values: Dict[str, str]) -> str:
        """Render template with values"""
        result = []
        for field, desc in self.fields.items():
            value = values.get(field, "")
            result.append(f"{desc}: {value}")
        return "\n".join(result)


# Common templates
TEMPLATES = {
    "bug": MemoryTemplate("bug", {
        "title": "Bug title",
        "severity": "Severity level",
        "description": "Bug description",
        "steps": "Steps to reproduce",
        "expected": "Expected behavior",
        "actual": "Actual behavior"
    }),
    "feature": MemoryTemplate("feature", {
        "title": "Feature name",
        "description": "Feature description",
        "benefit": "User benefit",
        "priority": "Priority"
    }),
    "meeting": MemoryTemplate("meeting", {
        "title": "Meeting title",
        "attendees": "Attendees",
        "date": "Date/time",
        "notes": "Notes",
        "action_items": "Action items"
    }),
    "feedback": MemoryTemplate("feedback", {
        "source": "Feedback source",
        "type": "Type (bug/feature/general)",
        "content": "Feedback content",
        "priority": "Priority"
    }),
}


class TemplateMemory:
    """Memory with template support"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add_from_template(self, template_name: str, values: Dict[str, str]) -> str:
        """Add memory from template"""
        if template_name not in TEMPLATES:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = TEMPLATES[template_name]
        content = template.render(values)
        
        return self.memory.add(content, tags=[template_name])
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(TEMPLATES.keys())


def demo():
    """Demo templates"""
    memory = Memory(storage="json", path="./template_demo.json")
    tm = TemplateMemory(memory)
    
    print("=== Memory Templates Demo ===\n")
    
    # List templates
    print(f"Available: {tm.list_templates()}\n")
    
    # Add from templates
    tm.add_from_template("bug", {
        "title": "Login crash",
        "severity": "High",
        "description": "App crashes on login",
        "steps": "1. Open app\n2. Click login\n3. Crash",
        "expected": "Login success",
        "actual": "Crash"
    })
    
    tm.add_from_template("feature", {
        "title": "Dark mode",
        "description": "Add dark mode option",
        "benefit": "Better user experience",
        "priority": "Medium"
    })
    
    print("Added 2 templated memories\n")
    
    # Show
    for mem in memory.get_all():
        print(f"Tags: {mem.get('tags')}")
        print(f"Content: {mem.get('content')[:80]}...")
        print()
    
    # Cleanup
    import os
    if os.path.exists("./template_demo.json"):
        os.remove("./template_demo.json")


if __name__ == "__main__":
    demo()
