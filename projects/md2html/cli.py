#!/usr/bin/env python3
"""
Markdown to HTML Converter
"""

import argparse
import re

def convert(md):
    """Simple markdown to HTML."""
    html = md
    
    # Headers
    for i in range(6, 0, -1):
        html = re.sub(rf'^{"#"*i} (.+)$', rf'<h{i}>\1</h{i>', html, flags=re.M)
    
    # Bold/Italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # Code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.M)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html)
    
    return f"<html><body>{html}</body></html>"

def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML")
    parser.add_argument("file", nargs="?", help="Input file (or stdin)")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file) as f:
            md = f.read()
    else:
        import sys
        md = sys.stdin.read()
    
    html = convert(md)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(html)
        print(f"Written to {args.output}")
    else:
        print(html)

if __name__ == "__main__":
    main()