"""
Memory Strategy
Strategy pattern for memory
"""
from memory import Memory


class SearchStrategy:
    """Search strategy"""
    def search(self, memory: Memory, query: str):
        raise NotImplementedError


class SimpleSearch(SearchStrategy):
    """Simple search"""
    def search(self, memory: Memory, query: str):
        return memory.search(query)


class AdvancedSearch(SearchStrategy):
    """Advanced search"""
    def search(self, memory: Memory, query: str):
        results = memory.search(query)
        # Filter results
        return [r for r in results if len(r.get("content", "")) > 10]


class ContextSearch(SearchStrategy):
    """Context search"""
    def search(self, memory: Memory, query: str):
        results = memory.search(query)
        # Add context
        return [{**r, "context": "found"} for r in results]


class StrategicMemory:
    """Memory with strategies"""
    def __init__(self, memory: Memory, strategy: SearchStrategy = None):
        self.memory = memory
        self.strategy = strategy or SimpleSearch()
    
    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy
    
    def search(self, query: str):
        return self.strategy.search(self.memory, query)


def demo():
    """Demo strategy"""
    memory = Memory(storage="json", path="./strategy_demo.json")
    
    sm = StrategicMemory(memory, SimpleSearch())
    am = StrategicMemory(memory, AdvancedSearch())
    
    memory.add("Test")
    
    print(f"Simple: {len(sm.search('test'))}")
    print(f"Advanced: {len(am.search('test'))}")


if __name__ == "__main__":
    demo()
