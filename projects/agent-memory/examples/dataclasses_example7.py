"""
Memory dataclasses_example7
dataclasses_example7
"""
from dataclasses import dataclass, field


@dataclass
class Inventory:
    items: dict = field(default_factory=dict)
    
    def add(self, name: str, quantity: int):
        self.items[name] = self.items.get(name, 0) + quantity


def demo():
    inv = Inventory()
    inv.add("apple", 10)
    inv.add("banana", 5)
    print(inv.items)


if __name__ == "__main__":
    demo()
