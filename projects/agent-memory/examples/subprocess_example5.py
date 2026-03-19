"""
Memory subprocess_example5
subprocess_example5
"""
import subprocess


def demo():
    p = subprocess.Popen(["echo", "hello"], stdout=subprocess.PIPE)
    print(p.stdout.read().decode().strip())


if __name__ == "__main__":
    demo()
