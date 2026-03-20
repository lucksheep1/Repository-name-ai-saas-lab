"""
Memory warnings_example8
warnings_example8
"""
import warnings


def demo():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        warnings.warn("This is a warning")
        print(len(w))


if __name__ == "__main__":
    demo()
