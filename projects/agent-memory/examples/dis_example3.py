"""
Memory dis_example3
dis_example3
"""
import dis


def demo():
    def add(a, b):
        return a + b
    dis.dis(add)


if __name__ == "__main__":
    demo()
