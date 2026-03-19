"""
Memory Signal
Signal/slot pattern
"""
from memory import Memory


class Signal:
    def __init__(self):
        self.slots = []
    
    def connect(self, slot):
        self.slots.append(slot)
    
    def emit(self, *args):
        for slot in self.slots:
            slot(*args)


def demo():
    signal = Signal()
    signal.connect(lambda x: print(f"Received: {x}"))
    signal.emit("Hello")


if __name__ == "__main__":
    demo()
