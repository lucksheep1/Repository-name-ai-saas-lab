"""
Memory warnings_example11
warnings_example11
"""
import warnings


def demo():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        warnings.warn("test")
        print(len(w))


if __name__ == "__main__":
    demo()
