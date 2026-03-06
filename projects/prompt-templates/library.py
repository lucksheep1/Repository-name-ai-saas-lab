#!/usr/bin/env python3
"""
Prompt Templates Library v2
Reusable prompts for AI development.
"""
from typing import Dict, Any, Optional
import os


TEMPLATES = {
    # ORIGINAL TEMPLATES
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
    },
    
    # NEW TEMPLATES v2
    "write-documentation": {
        "description": "Generate documentation for code",
        "template": """Generate documentation for the following {language} code:

Code:
```{language}
{code}
```

Include:
- Overview
- Function/method descriptions
- Parameters
- Return values
- Examples""",
        "variables": ["language", "code"]
    },
    
    "create-readme": {
        "description": "Create README for a project",
        "template": """Create a README for a project:

Project name: {project_name}
Description: {description}
Language: {language}
Features:
{features}

Include:
- Badges
- Installation
- Usage
- Contributing
- License""",
        "variables": ["project_name", "description", "language", "features"]
    },
    
    "write-sql": {
        "description": "Generate SQL queries",
        "template": """Write a SQL query for:

Task: {task}
Database type: {db_type}
Table structure: {table_schema}

Requirements:
{requirements}

Provide the SQL query with explanation.""",
        "variables": ["task", "db_type", "table_schema", "requirements"]
    },
    
    "create-api-spec": {
        "description": "Create API specification",
        "template": """Create an API specification for:

API name: {api_name}
Description: {description}
Language: {language}

Include:
- Endpoints
- Request/response formats
- Error handling
- Authentication""",
        "variables": ["api_name", "description", "language"]
    },
    
    "write-unit-test-prompt": {
        "description": "Create a prompt for writing tests",
        "template": """Create a comprehensive test prompt for:

Language: {language}
Framework: {framework}
Code to test:
```{language}
{code}
```

Include:
- Test cases
- Edge cases
- Mock objects
- Assertions""",
        "variables": ["language", "framework", "code"]
    },
    
    "security-audit": {
        "description": "Security audit for code",
        "template": """Perform a security audit on:

Language: {language}
Code:
```{language}
{code}
```

Check for:
- SQL injection
- XSS vulnerabilities
- Authentication issues
- Data exposure
- Common OWASP top 10 issues""",
        "variables": ["language", "code"]
    },
    
    "performance-optimize": {
        "description": "Performance optimization suggestions",
        "template": """Analyze and optimize the following {language} code for performance:

Code:
```{language}
{code}
```

Identify:
- Bottlenecks
- Memory issues
- Algorithmic improvements
- Caching opportunities""",
        "variables": ["language", "code"]
    },
    
    "write-git-commit": {
        "description": "Generate git commit message",
        "template": """Generate a git commit message for:

Changed files:
{files}

Diff summary:
{summary}

Use conventional commits format.""",
        "variables": ["files", "summary"]
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
    
    parser = argparse.ArgumentParser(description='Prompt Templates v2')
    subparsers = parser.add_subparsers()
    
    list_parser = subparsers.add_parser('list', help='List templates')
    
    gen_parser = subparsers.add_parser('generate', help='Generate a prompt')
    gen_parser.add_argument('name', help='Template name')
    gen_parser.add_argument('--var', action='append', help='Variables (key=value)')
    
    args = parser.parse_args()
    
    if hasattr(args, 'name'):
        template = Template.get(args.name)
        kwargs = {}
        if args.var:
            for v in args.var:
                if '=' in v:
                    key, value = v.split('=', 1)
                    kwargs[key] = value
        if not template.validate(**kwargs):
            print(f"Missing variables. Required: {template.variables}")
            return
        print(template.render(**kwargs))
    else:
        templates = Template.list_templates()
        print(f"Available templates ({len(templates)}):\n")
        for name, desc in templates.items():
            print(f"  {name}: {desc}")


if __name__ == '__main__':
    main()
