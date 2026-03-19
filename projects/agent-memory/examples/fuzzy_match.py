"""
Memory Fuzzy Match
Fuzzy string matching
"""
from memory import Memory


def levenshtein(s1: str, s2: str) -> int:
    """Levenshtein distance"""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    prev = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        
        for j, c2 in enumerate(s2):
            insertions = prev[j + 1] + 1
            deletions = curr[j] + 1
            substitutions = prev[j] + (c1 != c2)
            curr.append(min(insertions, deletions, substitutions))
        
        prev = curr
    
    return prev[-1]


class FuzzyMatch:
    """Fuzzy matching"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def search(self, query: str, threshold: int = 3):
        """Fuzzy search"""
        results = []
        
        for mem in self.memory.get_all():
            content = mem.get("content", "")
            
            words = content.split()
            
            for word in words:
                dist = levenshtein(query.lower(), word.lower())
                
                if dist <= threshold:
                    results.append({**mem, "match": word, "distance": dist})
                    break
        
        return sorted(results, key=lambda x: x["distance"])


def demo():
    """Demo fuzzy"""
    memory = Memory(storage="json", path="./fuzzy_demo2.json")
    fm = FuzzyMatch(memory)
    
    memory.add("Python programming")
    
    results = fm.search("python")
    print(f"Results: {len(results)}")


if __name__ == "__main__":
    demo()
