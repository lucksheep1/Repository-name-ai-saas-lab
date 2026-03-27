#!/usr/bin/env python3
"""
Word Count - Count words, lines, chars
"""

import argparse
import sys

def count(text):
    lines = text.count("\n") + 1
    words = len(text.split())
    chars = len(text)
    return {"lines": lines, "words": words, "chars": chars}

def main():
    parser = argparse.ArgumentParser(description="Word Count")
    parser.add_argument("file", nargs="?", help="File (or stdin)")
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file) as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    c = count(text)
    print(f"Lines: {c['lines']}")
    print(f"Words: {c['words']}")
    print(f"Chars: {c['chars']}")

if __name__ == "__main__":
    main()