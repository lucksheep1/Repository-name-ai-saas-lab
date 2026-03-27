#!/usr/bin/env python3
"""
Time Converter - Convert timestamps
"""

import argparse
from datetime import datetime

def to_unix(ts):
    return int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp())

def from_unix(ts):
    return datetime.fromtimestamp(int(ts)).isoformat()

def now_unix():
    return int(datetime.now().timestamp())

def now_iso():
    return datetime.now().isoformat()

def main():
    parser = argparse.ArgumentParser(description="Time Converter")
    parser.add_argument("time", nargs="?", help="Time to convert")
    parser.add_argument("--to-unix", action="store_true", help="Convert to Unix")
    parser.add_argument("--from-unix", action="store_true", help="Convert from Unix")
    parser.add_argument("--now", action="store_true", help="Show current time")
    
    args = parser.parse_args()
    
    if args.now:
        print(f"Unix: {now_unix()}")
        print(f"ISO: {now_iso()}")
    elif args.to_unix and args.time:
        print(to_unix(args.time))
    elif args.from_unix and args.time:
        print(from_unix(args.time))
    else:
        print(f"Unix: {now_unix()}")
        print(f"ISO: {now_iso()}")

if __name__ == "__main__":
    main()