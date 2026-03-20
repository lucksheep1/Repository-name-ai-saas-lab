"""
Memory argparse_example18
argparse_example18
"""
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="World")
    args = parser.parse_args([])
    print(f"Hello {args.name}")


if __name__ == "__main__":
    demo()
