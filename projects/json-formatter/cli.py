#!/usr/bin/env python3
"""
JSON Formatter - Format and validate JSON
"""

import argparse
import json
import sys

def format_json(data, indent=2):
    """Format JSON data."""
    return json.dumps(data, indent=indent, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="JSON Formatter")
    parser.add_argument("file", nargs="?", help="File to format (or stdin)")
    parser.add_argument("-i", "--indent", type=int, default=2, help="Indent spaces")
    parser.add_argument("-c", "--compact", action="store_true", help="Compact output")
    parser.add_argument("-v", "--validate", action="store_true", help="Only validate, no output")
    
    args = parser.parse_args()
    
    try:
        if args.file:
            with open(args.file, "r") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
        
        if args.validate:
            print("✅ Valid JSON")
            return
        
        if args.compact:
            print(json.dumps(data, separators=(",", ":")))
        else:
            print(json.dumps(data, indent=args.indent))
            
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

if __name__ == "__main__":
    main()