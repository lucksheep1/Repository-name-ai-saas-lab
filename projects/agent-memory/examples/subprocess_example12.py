"""
Memory subprocess_example12
subprocess_example12
"""
import subprocess


def demo():
    p = subprocess.Popen(["echo", "hello"], stdout=subprocess.PIPE)
    print(p.stdout.read().decode())


if __name__ == "__main__":
    demo()
