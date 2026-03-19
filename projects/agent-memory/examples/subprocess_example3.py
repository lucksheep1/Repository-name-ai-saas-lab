"""
Memory subprocess_example3
subprocess_example3
"""
import subprocess


def demo():
    p = subprocess.Popen(["echo", "hello"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    print(stdout.decode())


if __name__ == "__main__":
    demo()
