"""
Memory traceback_example10
traceback_example10
"""
import traceback


def demo():
    try:
        raise ValueError("test")
    except ValueError:
        print(traceback.format_exc())


if __name__ == "__main__":
    demo()
