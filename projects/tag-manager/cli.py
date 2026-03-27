#!/usr/bin/env python3
"""
Tag Manager - Organize project tags
"""

import argparse
import json
import os
from pathlib import Path

TAGS_FILE = ".project-tags.json"

def load_tags(path=None):
    """Load tags from file."""
    path = path or TAGS_FILE
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_tags(tags, path=None):
    """Save tags to file."""
    path = path or TAGS_FILE
    with open(path, "w") as f:
        json.dump(tags, f, indent=2)

def add_tag(tag, project, path=None):
    """Add a tag to a project."""
    tags = load_tags(path)
    if tag not in tags:
        tags[tag] = []
    if project not in tags[tag]:
        tags[tag].append(project)
    save_tags(tags, path)
    print(f"✅ Added {project} to {tag}")

def list_tags(path=None):
    """List all tags."""
    tags = load_tags(path)
    if not tags:
        print("No tags yet.")
        return
    print(f"📁 {len(tags)} tags:\n")
    for tag, projects in sorted(tags.items(), key=lambda x: -len(x[1])):
        print(f"  {tag} ({len(projects)}):")
        for p in projects:
            print(f"    - {p}")

def find_projects(tag, path=None):
    """Find projects by tag."""
    tags = load_tags(path)
    if tag not in tags:
        print(f"No projects with tag '{tag}'")
        return
    print(f"Projects with '{tag}':")
    for p in tags[tag]:
        print(f"  - {p}")

def main():
    parser = argparse.ArgumentParser(description="Tag Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add", help="Add tag")
    add_parser.add_argument("tag")
    add_parser.add_argument("project")
    
    subparsers.add_parser("list", help="List tags")
    
    find_parser = subparsers.add_parser("find", help="Find projects")
    find_parser.add_argument("tag")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_tag(args.tag, args.project)
    elif args.command == "list":
        list_tags()
    elif args.command == "find":
        find_projects(args.tag)

if __name__ == "__main__":
    main()