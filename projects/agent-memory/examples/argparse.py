"""
Memory Argparse
Argparse utilities
"""
from memory import Memory
import argparse


def demo():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name")
    args = parser.parse_args([])
    print(args.name)


if __name__ == "__main__":
    demo()
