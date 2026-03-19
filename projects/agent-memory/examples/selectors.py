"""
Memory selectors
selectors utilities
"""
import selectors


def demo():
    sel = selectors.DefaultSelector()
    print(sel)


if __name__ == "__main__":
    demo()
