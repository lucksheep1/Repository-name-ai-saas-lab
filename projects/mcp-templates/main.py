#!/usr/bin/env python3
"""
MCP Templates CLI - Quick-start templates for MCP servers.
"""
import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from generator import create_project, list_templates


def main():
    parser = argparse.ArgumentParser(
        description="MCP Templates - Quick-start templates for MCP servers"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # New command
    new_parser = subparsers.add_parser("new", help="Create a new MCP server")
    new_parser.add_argument("name", help="Name of the MCP server")
    new_parser.add_argument("--template", "-t", 
                          default="database",
                          choices=list_templates(),
                          help="Template to use")
    new_parser.add_argument("--output", "-o", 
                          default=".",
                          help="Output directory")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available templates")
    
    args = parser.parse_args()
    
    if args.command == "new":
        output_path = os.path.join(args.output, args.name)
        print(f"Creating MCP server: {args.name}")
        print(f"Template: {args.template}")
        print(f"Output: {output_path}")
        
        try:
            create_project(args.name, args.template)
            print(f"✓ Created {args.name}/")
            print(f"\nTo run:")
            print(f"  cd {args.name}")
            print(f"  pip install -r requirements.txt")
            print(f"  python main.py")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.command == "list":
        templates = list_templates()
        print("Available templates:")
        for t in templates:
            print(f"  - {t}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
