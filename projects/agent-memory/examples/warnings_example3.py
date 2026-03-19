"""
Memory warnings_example3
warnings_example3
"""
import warnings


def demo():
    warnings.filterwarnings("error")
    try:
        warnings.warn("error warning")
    except:
        print("caught")


if __name__ == "__main__":
    demo()
