"""
Memory dis_example4
dis_example4
"""
import dis


def demo():
    def foo():
        x = 1
        return x
    dis.dis(foo)


if __name__ == "__main__":
    demo()
