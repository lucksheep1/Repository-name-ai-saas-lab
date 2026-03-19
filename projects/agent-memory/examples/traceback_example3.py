"""
Memory traceback_example3
traceback_example3
"""
import traceback


def demo():
    try:
        raise ValueError("test")
    except:
        traceback.print_exc()


if __name__ == "__main__":
    demo()
