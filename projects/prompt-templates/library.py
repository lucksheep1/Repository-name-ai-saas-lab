#!/usr/bin/env python3
"""
Prompt Templates Library
Reusable prompts for AI development.
"""
from typing import Dict, Any, Optional
import os


TEMPLATES = {
    "code-generation": {
        "description": "Generate code from description",
        "template": """You are an expert {language} developer. Write code that accomplishes the following:

Task: {task}

Requirements:
{requirements}

Provide clean, well-documented code with comments.""",
        "variables": ["language", "task", "requirements"]
    },
    
    "code-review": {
        "description": "Review code for issues",
        "template": """You are a code reviewer. Review the following {language} code for:
- Security vulnerabilities
- Performance issues  
- Code style violations
- Potential bugs
- Best practices

Code:
```{language}
{code}
```

Provide a detailed report with:
1. Issue description
2. Line number (if applicable)
3. Severity (HIGH/MEDIUM/LOW)
4. Recommendation""",
        "variables": ["language", "code"]
    },
    
    "summarize": {
        "description": "Summarize long text",
        "template": """Summarize the following text in {max_length} words or less:

{text}

Summary should:
- Capture key points
- Be concise and clear
- Maintain original meaning""",
        "variables": ["max_length", "text"]
    },
    
    "translate": {
        "description": "Translate between languages",
        "template": """Translate the following {source_lang} text to {target_lang}:

{text}

Translation should:
- Preserve meaning
- Sound natural in {target_lang}
- Maintain formatting""",
        "variables": ["source_lang", "target_lang", "text"]
    },
    
    "explain": {
        "description": "Explain complex concepts",
        "template": """Explain the following concept in simple terms:

Concept: {concept}

Target audience: {audience}

Include:
- Simple definition
- Real-world examples
- Common use cases""",
        "variables": ["concept", "audience"]
    },
    
    "debug": {
        "description": "Debug code errors",
        "template": """Debug the following {language} code:

Error message:
{error}

Code:
```{language}
{code}
```

Provide:
1. Root cause analysis
2. Suggested fix
3. Explanation""",
        "variables": ["language", "error", "code"]
    },
    
    "test-generation": {
        "description": "Generate unit tests",
        "template": """Write unit tests for the following {language} code:

Code:
```{language}
{code}
```

Testing framework: {framework}

Include:
- Unit tests
- Edge cases
- Mock any external dependencies""",
        "variables": ["language", "code", "framework"]
    },
    
    "refactor": {
        "description": "Refactor code",
        "template": """Refactor the following {language} code to improve:
- Readability
- Performance
- Maintainability

Code:
```{language}
{code}
```

Provide refactored code with explanation of changes.""",
        "variables": ["language", "code"]
    }
}


class Template:
    """Prompt template handler."""
    
    @staticmethod
    def list_templates() -> Dict[str, str]:
        """List all available templates."""
        return {name: info["description"] for name, info in TEMPLATES.items()}
    
    @staticmethod
    def get(name: str) -> 'Template':
        """Get a template by name."""
        if name not in TEMPLATES:
            raise ValueError(f"Template '{name}' not found. Available: {list(TEMPLATES.keys())}")
        return Template(name, TEMPLATES[name])
    
    def __init__(self, name: str, data: Dict):
        self.name = name
        self.template = data["template"]
        self.variables = data["variables"]
    
    def render(self, **kwargs) -> str:
        """Render template with variables."""
        # Check required variables
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        
        return self.template.format(**kwargs)
    
    def validate(self, **kwargs) -> bool:
        """Check if all required variables are provided."""
        return set(self.variables).issubset(set(kwargs.keys()))


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Prompt Templates')
    subparsers = parser.add_subparsers()
    
    # list command
    list_parser = subparsers.add_parser('list', help='List templates')
    
    # generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a prompt')
    gen_parser.add_argument('name', help='Template name')
    gen_parser.add_argument('--var', action='append', help='Variables (key=value)')
    
    args = parser.parse_args()
    
    if hasattr(args, 'name'):
        # Generate
        template = Template.get(args.name)
        
        # Parse variables
        kwargs = {}
        if args.var:
            for v in args.var:
                if '=' in v:
                    key, value = v.split('=', 1)
                    kwargs[key] = value
        
        # Check if all variables provided
        if not template.validate(**kwargs):
            print(f"Missing variables. Required: {template.variables}")
            print("Usage: --var key=value")
            return
        
        print(template.render(**kwargs))
    
    else:
        # List
        templates = Template.list_templates()
        print("Available templates:\n")
        for name, desc in templates.items():
            print(f"  {name}: {desc}")


if __name__ == '__main__':
    main()
