"""
Memory dis_example10
dis_example10
"""
import dis


def demo():
    def add(a, b):
        return a + b
    print(dis.dis(add))


if __name__ == "__main__":
    demo()
