"""
Memory traceback_example8
traceback_example8
"""
import traceback


def demo():
    try:
        1 / 0
    except:
        print(traceback.format_exc()[:50])


if __name__ == "__main__":
    demo()
