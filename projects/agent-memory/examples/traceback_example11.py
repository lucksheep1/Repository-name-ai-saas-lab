"""
Memory traceback_example11
traceback_example11
"""
import traceback


def demo():
    try:
        1 / 0
    except:
        traceback.print_exc()


if __name__ == "__main__":
    demo()
