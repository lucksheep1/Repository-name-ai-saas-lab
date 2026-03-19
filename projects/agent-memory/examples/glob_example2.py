"""
Memory glob_example2
glob_example2
"""
import glob


def demo():
    print(glob.glob("/tmp/*.txt", recursive=True)[:3])


if __name__ == "__main__":
    demo()
