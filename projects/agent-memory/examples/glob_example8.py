"""
Memory glob_example8
glob_example8
"""
import glob


def demo():
    for f in glob.iglob("**/*.py", recursive=True):
        if len(f) < 50:
            print(f)


if __name__ == "__main__":
    demo()
