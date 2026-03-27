#!/usr/bin/env python3
"""
Dependency Scanner - Find unused dependencies
"""

import argparse
import os
import re
from pathlib import Path

def find_imports(path):
    """Find all imports in Python files."""
    imports = set()
    for f in Path(path).rglob("*.py"):
        try:
            content = f.read_text()
            # Simple regex for imports
            for match in re.findall(r'^import\s+(\S+)', content, re.M):
                imports.add(match.split('.')[0])
            for match in re.findall(r'^from\s+(\S+)\s+import', content, re.M):
                imports.add(match.split('.')[0])
        except:
            pass
    return imports

def get_requirements(path):
    """Get requirements.txt contents."""
    req_file = Path(path) / "requirements.txt"
    if req_file.exists():
        return set(line.strip().split('==')[0].split('>=')[0].split('<=')[0] 
                   for line in req_file.read_text().split('\n') 
                   if line.strip() and not line.startswith('#'))
    return set()

def main():
    parser = argparse.ArgumentParser(description="Dependency Scanner")
    parser.add_argument("path", nargs="?", default=".", help="Project path")
    
    args = parser.parse_args()
    
    imports = find_imports(args.path)
    requirements = get_requirements(args.path)
    
    print(f"📦 Requirements: {len(requirements)}")
    print(f"🔍 Imports found: {len(imports)}")
    print()
    
    unused = requirements - imports
    if unused:
        print(f"⚠️  Possibly unused: {', '.join(sorted(unused))}")
    else:
        print("✅ All requirements appear used")

if __name__ == "__main__":
    main()