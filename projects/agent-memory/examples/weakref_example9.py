"""
Memory weakref_example9
weakref_example9
"""
import weakref


class Callback:
    def __init__(self, obj):
        self.ref = weakref.ref(obj, self.on_delete)
    
    def on_delete(self, ref):
        print("Object deleted!")


def demo():
    obj = object()
    cb = Callback(obj)
    del obj


if __name__ == "__main__":
    demo()
