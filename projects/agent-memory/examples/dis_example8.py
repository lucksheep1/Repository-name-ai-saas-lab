"""
Memory dis_example8
dis_example8
"""
import dis


def demo():
    def hello():
        print("Hello")
    dis.dis(hello)


if __name__ == "__main__":
    demo()
