#!/usr/bin/env python3
"""
Project Stats - Show project statistics at a glance
"""

import argparse
import os
import json
from pathlib import Path
from datetime import datetime

def scan_projects(root):
    """Scan all projects."""
    root = Path(root)
    projects = []
    
    for d in root.iterdir():
        if d.is_dir() and (d / "README.md").exists():
            # Count files
            py_files = list(d.rglob("*.py"))
            md_files = list(d.rglob("*.md"))
            all_files = list(d.rglob("*"))
            
            # Check for key files
            has_cli = (d / "cli.py").exists() or (d / "main.py").exists()
            has_status = (d / "STATUS.md").exists()
            
            # Try to get description
            readme = d / "README.md"
            desc = ""
            if readme.exists():
                try:
                    lines = readme.read_text().split("\n")
                    for line in lines:
                        if line and not line.startswith("#"):
                            desc = line.strip()[:60]
                            break
                except:
                    pass
            
            projects.append({
                "name": d.name,
                "py_files": len(py_files),
                "md_files": len(md_files),
                "total_files": len([f for f in all_files if f.is_file()]),
                "has_cli": has_cli,
                "has_status": has_status,
                "description": desc
            })
    
    return projects

def main():
    parser = argparse.ArgumentParser(description="Project Stats")
    parser.add_argument("path", nargs="?", default="projects", help="Projects directory")
    parser.add_argument("--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    projects = scan_projects(args.path)
    
    if args.json:
        print(json.dumps(projects, indent=2))
        return
    
    print(f"📊 Project Stats ({len(projects)} projects)\n")
    
    # Summary
    total_py = sum(p["py_files"] for p in projects)
    total_md = sum(p["md_files"] for p in projects)
    total_files = sum(p["total_files"] for p in projects)
    with_cli = sum(1 for p in projects if p["has_cli"])
    with_status = sum(1 for p in projects if p["has_status"])
    
    print(f"Total Files: {total_files}")
    print(f"Python Files: {total_py}")
    print(f"Markdown Files: {total_md}")
    print(f"With CLI: {with_cli}")
    print(f"With STATUS.md: {with_status}")
    print()
    
    # Table
    print(f"{'Name':<25} {'PY':>4} {'MD':>4} {'Files':>6} {'Status':<6}")
    print("-" * 55)
    
    for p in sorted(projects, key=lambda x: -x["total_files"]):
        status = "✅" if p["has_status"] else "❌"
        print(f"{p['name']:<25} {p['py_files']:>4} {p['md_files']:>4} {p['total_files']:>6} {status:<6}")

if __name__ == "__main__":
    main()