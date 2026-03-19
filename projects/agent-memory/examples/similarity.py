"""
Memory Similarity
Find similar memories
"""
from memory import Memory


class SimilarityFinder:
    """Find similar memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def find_similar(self, mem_id: str, threshold: float = 0.5):
        """Find similar memories"""
        target = self.memory.get(mem_id)
        
        if not target:
            return []
        
        target_words = set(target.get("content", "").lower().split())
        
        results = []
        
        for mem in self.memory.get_all():
            if mem["id"] == mem_id:
                continue
            
            mem_words = set(mem.get("content", "").lower().split())
            
            # Jaccard similarity
            if not target_words or not mem_words:
                continue
            
            intersection = len(target_words & mem_words)
            union = len(target_words | mem_words)
            
            similarity = intersection / union
            
            if similarity >= threshold:
                results.append({**mem, "similarity": similarity})
        
        return sorted(results, key=lambda x: x["similarity"], reverse=True)


def demo():
    """Demo similarity"""
    memory = Memory(storage="json", path="./similarity_demo.json")
    finder = SimilarityFinder(memory)
    
    memory.add("Python is great")
    memory.add("Python is awesome")
    memory.add("Java is different")
    
    mems = memory.get_all()
    
    if len(mems) >= 2:
        results = finder.find_similar(mems[0]["id"])
        print(f"Similar: {len(results)}")


if __name__ == "__main__":
    demo()
