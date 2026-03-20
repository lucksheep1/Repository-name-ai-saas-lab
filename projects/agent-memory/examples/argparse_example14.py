"""
Memory argparse_example14
argparse_example14
"""
import argparse


def demo():
    parser = argparse.ArgumentParser(prog="myapp")
    parser.add_argument("-v", "--version", action="version", version="1.0.0")
    args = parser.parse_args(["-v"])
    print(args)


if __name__ == "__main__":
    demo()
