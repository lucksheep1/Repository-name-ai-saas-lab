"""
Memory subprocess_example13
subprocess_example13
"""
import subprocess


def demo():
    p = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = p.communicate(b"hello")
    print(stdout.decode())


if __name__ == "__main__":
    demo()
