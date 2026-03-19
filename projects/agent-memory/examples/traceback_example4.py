"""
Memory traceback_example4
traceback_example4
"""
import traceback


def demo():
    try:
        1/0
    except:
        traceback.print_exc()


if __name__ == "__main__":
    demo()
