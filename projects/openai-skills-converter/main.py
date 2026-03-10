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

def convert_to_skill(prompt: str, name: str = None, description: str = None, 
                     tools: list = None, examples: list = None) -> dict:
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
    
    if tools:
        skill["tools"] = tools
    if examples:
        skill["examples"] = examples
    
    return skill

def validate_skill(skill: dict) -> bool:
    """Validate skill structure"""
    required = ["name", "description", "instructions"]
    for field in required:
        if not skill.get(field):
            print(f"Error: Missing required field: {field}")
            return False
    
    # Validate tools if present
    if skill.get("tools"):
        for tool in skill["tools"]:
            if not isinstance(tool, dict) or "name" not in tool:
                print("Error: Each tool must have a 'name' field")
                return False
    
    # Validate examples if present
    if skill.get("examples"):
        for ex in skill["examples"]:
            if not isinstance(ex, dict) or "input" not in ex or "output" not in ex:
                print("Error: Each example must have 'input' and 'output' fields")
                return False
    
    print("✅ Skill is valid!")
    print(f"   - Name: {skill['name']}")
    print(f"   - Description: {skill['description']}")
    print(f"   - Instructions: {len(skill['instructions'])} chars")
    print(f"   - Tools: {len(skill.get('tools', []))}")
    print(f"   - Examples: {len(skill.get('examples', []))}")
    return True

def add_tools_interactive() -> list:
    """Interactive tool builder"""
    tools = []
    print("\n=== Add Tools (empty to finish) ===")
    
    while True:
        name = input("Tool name (empty to finish): ").strip()
        if not name:
            break
        
        description = input("Tool description: ").strip()
        parameters = input("Tool parameters (JSON or description): ").strip()
        
        tool = {"name": name, "description": description}
        if parameters:
            try:
                tool["parameters"] = json.loads(parameters)
            except:
                tool["parameters"] = {"description": parameters}
        
        tools.append(tool)
        print(f"✅ Added tool: {name}")
    
    return tools

def add_examples_interactive() -> list:
    """Interactive example builder"""
    examples = []
    print("\n=== Add Examples (empty to finish) ===")
    
    while True:
        input_text = input("Example input (empty to finish): ").strip()
        if not input_text:
            break
        
        output_text = input("Example output: ").strip()
        
        example = {"input": input_text, "output": output_text}
        examples.append(example)
        print(f"✅ Added example {len(examples)}")
    
    return examples

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
    
    # Add tools
    skill["tools"] = add_tools_interactive()
    
    # Add examples
    skill["examples"] = add_examples_interactive()
    
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
        print("Usage: python main.py [convert|validate|interactive|batch|init|test]")
        print("")
        print("Commands:")
        print("  convert     - Convert a single prompt file to skill format")
        print("  validate    - Validate an existing skill JSON file")
        print("  interactive - Interactive skill builder with tools & examples")
        print("  batch       - Batch convert multiple prompt files")
        print("  init        - Initialize a new skill project")
        print("  test        - Test a skill with sample prompts")
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
    
    elif cmd == "init":
        # Initialize a new skill project
        name = input("Skill name: ").strip()
        description = input("Description: ").strip()
        
        skill_dir = Path(name.lower().replace(" ", "-"))
        skill_dir.mkdir(exist_ok=True)
        
        # Create skill.json
        skill = {
            "name": name,
            "description": description,
            "instructions": "# Your instructions here\n",
            "tools": [],
            "examples": []
        }
        (skill_dir / "skill.json").write_text(json.dumps(skill, indent=2))
        
        # Create README.md
        (skill_dir / "README.md").write_text(f"""# {name}

{description}

## Usage

Describe how to use this skill.

## Tools

List tools here.

## Examples

Add examples here.
""")
        
        print(f"✅ Initialized skill project: {skill_dir}/")
        print(f"   - skill.json")
        print(f"   - README.md")
    
    elif cmd == "test":
        # Test a skill with sample prompts
        if len(sys.argv) < 3:
            print("Usage: python main.py test <skill.json> [--prompts <dir>]")
            print("")
            print("Test your skill with sample prompts")
            print("  skill.json   - Path to skill file")
            print("  --prompts   - Optional directory with test prompts (.txt files)")
            sys.exit(1)
        
        skill_file = sys.argv[2]
        prompts_dir = None
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--prompts":
                prompts_dir = sys.argv[i+1]
                i += 2
            else:
                i += 1
        
        # Load skill
        skill = json.loads(Path(skill_file).read_text())
        print(f"\n🧪 Testing skill: {skill.get('name', 'Unknown')}")
        print(f"   Description: {skill.get('description', 'N/A')}")
        
        # Show skill structure
        print("\n📋 Skill Structure:")
        print(f"   - Instructions: {len(skill.get('instructions', ''))} chars")
        print(f"   - Tools: {len(skill.get('tools', []))}")
        print(f"   - Examples: {len(skill.get('examples', []))}")
        
        # Test with provided examples
        if skill.get("examples"):
            print("\n✅ Skill has examples - ready for testing")
            for i, ex in enumerate(skill["examples"], 1):
                print(f"\n   Example {i}:")
                print(f"   Input:  {ex.get('input', '')[:60]}...")
                print(f"   Output: {ex.get('output', '')[:60]}...")
        
        # Test with prompts directory
        if prompts_dir:
            prompts_path = Path(prompts_dir)
            if prompts_path.exists():
                print(f"\n📁 Testing with prompts from: {prompts_dir}")
                test_count = 0
                for prompt_file in prompts_path.glob("*.txt"):
                    content = prompt_file.read_text()
                    print(f"\n   📝 {prompt_file.name}:")
                    print(f"      {content[:80]}...")
                    test_count += 1
                print(f"\n✅ Loaded {test_count} test prompts")
            else:
                print(f"⚠️  Prompts directory not found: {prompts_dir}")
        
        print("\n💡 To test with OpenAI API, use the skill in Codex/Claude Code")
        print("=" * 40)
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
