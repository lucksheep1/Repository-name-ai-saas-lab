"""
Memory Auto-Tagging
Automatically tag memories based on content
"""
from agent_memory import Memory
import re


class AutoTagger:
    """Automatically tag memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.rules = []
    
    def add_rule(self, pattern: str, tag: str):
        """Add tagging rule"""
        self.rules.append((re.compile(pattern, re.I), tag))
    
    def tag(self, content: str) -> list:
        """Auto-tag content"""
        tags = []
        
        for pattern, tag in self.rules:
            if pattern.search(content):
                tags.append(tag)
        
        return tags
    
    def process(self, mem_id: str = None):
        """Process memories and add tags"""
        if mem_id:
            mems = [self.memory.get(mem_id)]
        else:
            mems = self.memory.get_all()
        
        tagged = 0
        
        for mem in mems:
            if not mem:
                continue
            
            current_tags = set(mem.get("tags", []))
            new_tags = self.tag(mem.get("content", ""))
            
            # Add new tags
            updated = False
            for tag in new_tags:
                if tag not in current_tags:
                    current_tags.add(tag)
                    updated = True
            
            if updated:
                self.memory.update(mem_id, tags=list(current_tags))
                tagged += 1
        
        return tagged


# Default rules
DEFAULT_RULES = [
    (r"\berror\b|\bexception\b|\bbug\b|\bcrash\b", "bug"),
    (r"\bugent\b|\bcritical\b|\basap\b", "urgent"),
    (r"\btodo\b|\btask\b|\baction\b", "action"),
    (r"\bquestion\b|\bhow to\b|\bhelp\b", "question"),
    (r"\bidea\b|\bsuggest\b|\bproposal\b", "idea"),
    (r"\bmeeting\b|\bcall\b|\bschedule\b", "schedule"),
    (r"\bpassword\b|\bsecret\b|\btoken\b", "sensitive"),
    (r"\bfix\b|\brepair\b|\bresolve\b", "fix"),
    (r"\bfeature\b|\benhancement\b|\badd\b", "feature"),
    (r"\breview\b|\bcheck\b|\bverify\b", "review"),
]


def demo():
    """Demo auto-tagging"""
    memory = Memory(storage="json", path="./autotag_demo.json")
    tagger = AutoTagger(memory)
    
    print("=== Auto-Tagger Demo ===\n")
    
    # Add default rules
    for pattern, tag in DEFAULT_RULES:
        tagger.add_rule(pattern, tag)
    
    # Add sample memories
    memory.add("Critical: system crashed", tags=[])
    memory.add("Bug in login flow", tags=[])
    memory.add("Todo: implement auth", tags=[])
    memory.add("Question: how does x work?", tags=[])
    memory.add("Good idea for new feature", tags=[])
    
    print("Added 5 memories (no tags)")
    
    # Auto-tag
    tagged = tagger.process()
    print(f"Auto-tagged {tagged} memories\n")
    
    # Show results
    for mem in memory.get_all():
        print(f"  {mem['content'][:40]}... → {mem.get('tags', [])}")
    
    # Cleanup
    import os
    if os.path.exists("./autotag_demo.json"):
        os.remove("./autotag_demo.json")


if __name__ == "__main__":
    demo()
