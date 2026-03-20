"""
Memory glob_example7
glob_example7
"""
import glob


def demo():
    import os
    print(glob.glob(os.path.join(os.getcwd(), "*.py")))


if __name__ == "__main__":
    demo()
