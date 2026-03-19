"""
Memory argparse_example7
argparse_example7
"""
import argparse


def demo():
    parser = argparse.ArgumentParser(prog="myapp")
    parser.add_argument("--version", action="version", version="1.0.0")
    args = parser.parse_args(["--version"])


if __name__ == "__main__":
    demo()
