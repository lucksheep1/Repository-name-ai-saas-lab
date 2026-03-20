"""
Memory dis_example11
dis_example11
"""
import dis


def demo():
    def add(a, b):
        return a + b
    dis.dis(add)


if __name__ == "__main__":
    demo()
