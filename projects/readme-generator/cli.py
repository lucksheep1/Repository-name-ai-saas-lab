#!/usr/bin/env python3
"""
README Generator - Generate README.md from project structure
"""

import argparse
import os
import sys
from pathlib import Path

TEMPLATE = """# {name}

{description}

## Installation

```bash
pip install {name}
```

## Usage

```bash
{usage_example}
```

## Features

{features}

## Verification

- [ ] Tested locally

---
*Generated: {date}*
"""

FEATURES_TEMPLATE = """- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3
"""

def scan_project(path):
    """Scan project structure."""
    path = Path(path)
    
    files = []
    for f in path.rglob("*"):
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(path)
            files.append(str(rel))
    
    # Check for key files
    has_py = any(f.endswith(".py") for f in files)
    has_readme = "README.md" in files
    has_requirements = "requirements.txt" in files
    has_pyproject = "pyproject.toml" in files
    
    return {
        "files": files[:20],  # First 20
        "has_py": has_py,
        "has_readme": has_readme,
        "has_requirements": has_requirements,
        "has_pyproject": has_pyproject
    }

def generate_readme(project_path, name=None, description=None):
    """Generate README.md."""
    path = Path(project_path)
    name = name or path.name
    
    info = scan_project(path)
    
    if description is None:
        description = f"A Python project: {name}"
    
    features = FEATURES_TEMPLATE
    
    # Try to detect main file
    main_file = None
    for f in info["files"]:
        if f.endswith(".py") and not f.startswith("test"):
            main_file = f
            break
    
    if main_file:
        usage = f"python {main_file}"
    else:
        usage = f"python main.py"
    
    readme = TEMPLATE.format(
        name=name,
        description=description,
        usage_example=usage,
        features=features,
        date="2026-03-27"
    )
    
    return readme

def main():
    parser = argparse.ArgumentParser(description="README Generator")
    parser.add_argument("path", nargs="?", default=".", help="Project path")
    parser.add_argument("-n", "--name", help="Project name")
    parser.add_argument("-d", "--description", help="Project description")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    readme = generate_readme(args.path, args.name, args.description)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(readme)
        print(f"✅ Generated {args.output}")
    else:
        print(readme)

if __name__ == "__main__":
    main()
