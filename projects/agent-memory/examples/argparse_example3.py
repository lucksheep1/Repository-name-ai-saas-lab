"""
Memory argparse_example3
argparse_example3
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("pos", help="positional arg")
    args = parser.parse_args(["value"])
    print(args.pos)


if __name__ == "__main__":
    demo()
