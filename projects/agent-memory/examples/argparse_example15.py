"""
Memory argparse_example15
argparse_example15
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("age", type=int)
    args = parser.parse_args(["Alice", "30"])
    print(f"{args.name} is {args.age} years old")


if __name__ == "__main__":
    demo()
