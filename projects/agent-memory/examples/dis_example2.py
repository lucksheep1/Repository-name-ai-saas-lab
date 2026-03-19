"""
Memory dis_example2
dis_example2
"""
import dis


def demo():
    def foo():
        return 1 + 2
    dis.dis(foo)


if __name__ == "__main__":
    demo()
