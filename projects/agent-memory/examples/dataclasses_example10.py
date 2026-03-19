"""
Memory dataclasses_example10
dataclasses_example10
"""
from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    price: float
    quantity: int = 1
    
    def total(self) -> float:
        return self.price * self.quantity


def demo():
    item = Item("Apple", 0.5, 10)
    print(item.total())


if __name__ == "__main__":
    demo()
