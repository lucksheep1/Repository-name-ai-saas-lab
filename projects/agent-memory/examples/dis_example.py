"""
Memory dis_example
dis_example
"""
import dis


def demo():
    def foo():
        return 1
    dis.dis(foo)


if __name__ == "__main__":
    demo()
