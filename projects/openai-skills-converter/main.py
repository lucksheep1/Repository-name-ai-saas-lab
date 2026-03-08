#!/usr/bin/env python3
"""
OpenAI Skills Converter
Convert prompts to OpenAI Skills format (openai/skills)
"""

import json
import sys
from pathlib import Path

SKILL_SCHEMA = {
    "name": "",
    "description": "",
    "instructions": "",
    "tools": [],
    "examples": []
}

def load_prompt(path: str) -> str:
    """Load prompt from file"""
    p = Path(path)
    if not p.exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)
    return p.read_text()

def convert_to_skill(prompt: str, name: str = None, description: str = None) -> dict:
    """Convert prompt to OpenAI Skills format"""
    skill = SKILL_SCHEMA.copy()
    
    if name:
        skill["name"] = name
    else:
        skill["name"] = input("Skill name: ").strip()
    
    if description:
        skill["description"] = description
    else:
        skill["description"] = input("Description: ").strip()
    
    skill["instructions"] = prompt.strip()
    
    return skill

def validate_skill(skill: dict) -> bool:
    """Validate skill structure"""
    required = ["name", "description", "instructions"]
    for field in required:
        if not skill.get(field):
            print(f"Error: Missing required field: {field}")
            return False
    print("✅ Skill is valid!")
    return True

def batch_convert(input_dir: str, output_dir: str) -> int:
    """Batch convert multiple prompt files to skills"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not input_path.exists():
        print(f"Error: Directory not found: {input_dir}")
        sys.exit(1)
    
    count = 0
    for prompt_file in input_path.glob("*.txt"):
        name = prompt_file.stem.replace("_", " ").title()
        description = f"Auto-generated skill from {prompt_file.name}"
        
        prompt = prompt_file.read_text()
        skill = convert_to_skill(prompt, name, description)
        
        output_file = output_path / f"{prompt_file.stem}.json"
        output_file.write_text(json.dumps(skill, indent=2))
        print(f"✅ Converted: {prompt_file.name} -> {output_file.name}")
        count += 1
    
    print(f"\n📦 Batch complete: {count} skills converted")
    return count

def interactive_mode():
    """Interactive skill builder"""
    print("\n=== OpenAI Skills Builder ===\n")
    
    skill = SKILL_SCHEMA.copy()
    skill["name"] = input("Skill name: ").strip()
    skill["description"] = input("Description: ").strip()
    print("\nInstructions (Ctrl+D to finish):")
    skill["instructions"] = sys.stdin.read().strip()
    
    print("\n=== Generated Skill ===\n")
    print(json.dumps(skill, indent=2))
    
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save == "y":
        filename = f"{skill['name'].lower().replace(' ', '_')}.json"
        Path(filename).write_text(json.dumps(skill, indent=2))
        print(f"✅ Saved to {filename}")
    
    return skill

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [convert|validate|interactive|batch]")
        print("")
        print("Commands:")
        print("  convert     - Convert a single prompt file to skill format")
        print("  validate    - Validate an existing skill JSON file")
        print("  interactive - Interactive skill builder")
        print("  batch       - Batch convert multiple prompt files")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "convert":
        if len(sys.argv) < 4:
            print("Usage: python main.py convert --input <file> [--name <name>] [--description <desc>] [--output <file>]")
            sys.exit(1)
        
        input_file = None
        name = None
        description = None
        output_file = "skill.json"
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--input":
                input_file = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--name":
                name = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--description":
                description = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--output":
                output_file = sys.argv[i+1]
                i += 2
            else:
                i += 1
        
        if not input_file:
            print("Error: --input required")
            sys.exit(1)
        
        prompt = load_prompt(input_file)
        skill = convert_to_skill(prompt, name, description)
        
        Path(output_file).write_text(json.dumps(skill, indent=2))
        print(f"✅ Saved to {output_file}")
    
    elif cmd == "validate":
        if len(sys.argv) < 3:
            print("Usage: python main.py validate <skill.json>")
            sys.exit(1)
        
        skill_file = sys.argv[2]
        skill = json.loads(Path(skill_file).read_text())
        validate_skill(skill)
    
    elif cmd == "interactive":
        interactive_mode()
    
    elif cmd == "batch":
        if len(sys.argv) < 4:
            print("Usage: python main.py batch --input-dir <dir> [--output-dir <dir>]")
            sys.exit(1)
        
        input_dir = None
        output_dir = "skills_output"
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--input-dir":
                input_dir = sys.argv[i+1]
                i += 2
            elif sys.argv[i] == "--output-dir":
                output_dir = sys.argv[i+1]
                i += 2
            else:
                i += 1
        
        if not input_dir:
            print("Error: --input-dir required")
            sys.exit(1)
        
        batch_convert(input_dir, output_dir)
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
