"""
Memory warnings_example10
warnings_example10
"""
import warnings


def demo():
    warnings.filterwarnings("error")
    try:
        warnings.warn("Error!")
    except UserWarning:
        print("Caught!")


if __name__ == "__main__":
    demo()
