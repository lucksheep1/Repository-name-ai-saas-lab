"""
Memory warnings_example9
warnings_example9
"""
import warnings


def demo():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        warnings.warn("This will be ignored")


if __name__ == "__main__":
    demo()
