# Prompt Templates Library

Reusable prompt templates for AI development.

## Problem

Developers keep rewriting similar prompts:
- Code generation prompts
- Summarization prompts
- Translation prompts
- Analysis prompts

## Solution

A library of reusable prompt templates:
- **Organized** by use case
- **Customizable** variables
- **CLI** to generate prompts

## Installation

```bash
pip install prompt-templates
```

## Usage

```bash
# List available templates
prompt-templates list

# Generate a prompt
prompt-templates generate code-review --language python

# Generate with custom variables
prompt-templates generate summarize --max-length 500
```

## Templates

### code-generation
Generate code from description.

### code-review
Review code for issues.

### summarize
Summarize long text.

### translate
Translate between languages.

### explain
Explain complex concepts.

### debug
Debug code errors.

## Example

```bash
$ prompt-templates generate code-review --language python
You are a code reviewer. Review the following Python code for:
- Security vulnerabilities
- Performance issues
- Code style violations
- Potential bugs

Code:
{code}

Provide a detailed report with line numbers and recommendations.
```

## Library Usage

```python
from prompt_templates import Template

# Load a template
template = Template.get("code-review")

# Render with variables
prompt = template.render(
    language="python",
    code="def foo():\n    pass"
)

print(prompt)
```

## Next

- [ ] Add more templates
- [ ] Add template contributions
- [ ] Add community templates

---
*Built: 2026-03-06*
