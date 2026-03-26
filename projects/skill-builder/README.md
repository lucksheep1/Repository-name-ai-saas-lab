# skill-builder

**Generate OpenClaw SKILL.md files from templates.**

Builds properly formatted SKILL.md for the OpenClaw skill ecosystem, following the format established by [linux-server-skill](https://github.com/michael-ltm/linux-server-skill).

## Templates

| Template | Description |
|----------|-------------|
| `memory` | AI agent persistent memory management |
| `git` | Git history analysis and queries |
| `search` | Web search with Brave API |
| `server` | Linux server management via SSH |
| `monitor` | System resource monitoring and alerts |
| `scrape` | Web scraping and content extraction |

## Usage

```bash
# List all available templates
python skill_builder.py list

# Generate a skill from a template
python skill_builder.py new git-history --desc "Analyze git history" --triggers "git log,commits"

# Generate from built-in template
python skill_builder.py new agent-memory-ops --template memory

# Generate fully custom skill
python skill_builder.py generate my-custom-skill --desc "Does X" --triggers "do X,start X"
```

## Generated SKILL.md Format

```yaml
---
name: <skill-name>
description: <description>
---

# Skill Name

## When to Use

Use this skill when the user mentions: trigger1, trigger2, ...

## [Custom Sections]

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
```

## Installation

Copy the generated SKILL.md to your OpenClaw skills directory:

```bash
cp skills/agent-memory-ops/SKILL.md ~/.openclaw/skills/
```

## Skill Format Reference

The SKILL.md format (from linux-server-skill):
- YAML frontmatter with `name` and `description`
- Markdown body with usage instructions
- Sensitive data handling rules
- Session start checklist
- Command reference

## Verification

```bash
cd projects/skill-builder
python skill_builder.py list
# Should show 6 templates

python skill_builder.py new test-skill --desc "Test skill"
cat skills/test-skill/SKILL.md
```

## References

- [linux-server-skill](https://github.com/michael-ltm/linux-server-skill) — the reference SKILL.md format
- [OpenClaw Skills](https://docs.openclaw.ai/skills) — OpenClaw skill documentation
