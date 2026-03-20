"""
Memory argparse_example11
argparse_example11
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs="*")
    args = parser.parse_args(["a", "b", "c"])
    print(args.args)


if __name__ == "__main__":
    demo()
