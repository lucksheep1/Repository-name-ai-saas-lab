"""
Memory warnings_example5
warnings_example5
"""
import warnings


def demo():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warnings.warn("test")


if __name__ == "__main__":
    demo()
