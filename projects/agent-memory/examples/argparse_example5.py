"""
Memory argparse_example5
argparse_example5
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args(["-vvv"])
    print(args.verbose)


if __name__ == "__main__":
    demo()
