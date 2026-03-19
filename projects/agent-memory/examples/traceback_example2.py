"""
Memory traceback_example2
traceback_example2
"""
import traceback


def demo():
    try:
        raise ValueError("test")
    except:
        traceback.print_exc()


if __name__ == "__main__":
    demo()
