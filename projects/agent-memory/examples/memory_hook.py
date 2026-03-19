"""
Memory Hook
Hook system
"""
from memory import Memory


class Hook:
    def __init__(self):
        self.callbacks = []
    
    def register(self, callback):
        self.callbacks.append(callback)
    
    def trigger(self, *args):
        for cb in self.callbacks:
            cb(*args)


def demo():
    hook = Hook()
    hook.register(lambda: print("Called!"))
    hook.trigger()


if __name__ == "__main__":
    demo()
