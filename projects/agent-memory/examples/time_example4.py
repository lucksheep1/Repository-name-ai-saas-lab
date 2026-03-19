"""
Memory time_example4
time_example4
"""
import time


def demo():
    struct_time = time.localtime()
    print(time.strftime("%H:%M:%S", struct_time))


if __name__ == "__main__":
    demo()
