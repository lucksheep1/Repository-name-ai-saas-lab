"""
Memory subprocess
subprocess utilities
"""
from memory import Memory
import subprocess


def demo():
    result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    demo()
