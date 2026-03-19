"""
Memory warnings_example4
warnings_example4
"""
import warnings


def demo():
    with warnings.catch_warnings(record=True) as w:
        warnings.warn("test warning")
        print(len(w))


if __name__ == "__main__":
    demo()
