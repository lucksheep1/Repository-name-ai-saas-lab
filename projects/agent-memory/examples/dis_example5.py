"""
Memory dis_example5
dis_example5
"""
import dis


def demo():
    def f():
        x = 1
        return x
    dis.dis(f)


if __name__ == "__main__":
    demo()
