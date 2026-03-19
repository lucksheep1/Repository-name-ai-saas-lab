"""
Memory warnings_example2
warnings_example2
"""
import warnings


def demo():
    with warnings.catch_warnings(record=True) as w:
        warnings.warn("test warning")
        print(w[0].message)


if __name__ == "__main__":
    demo()
