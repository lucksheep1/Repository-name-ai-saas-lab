# OpenAI Skills Converter

Convert your prompts and instructions into OpenAI Skills format for Codex.

## Problem

OpenAI Skills (openai/skills) is trending with 12,697 stars. Developers want to create skills but need a simple way to convert existing prompts.

## Solution

A CLI tool that converts prompts/instructions into OpenAI Skills format.

## Usage

```bash
# Convert a prompt file to skill format
python main.py convert --input prompt.txt --output skill.json

# Convert with custom name and description
python main.py convert --input prompt.txt --name "Code Reviewer" --description "Reviews code for bugs"

# Batch convert multiple prompts
python main.py batch --input-dir ./prompts --output-dir ./skills

# Interactive mode
python main.py interactive

# Validate existing skill
python main.py validate skill.json
```

## Features

- ✅ Single prompt conversion
- ✅ Batch processing (multiple prompts at once)
- ✅ Interactive skill builder
- ✅ Skill validation

## Verification

✅ Converts prompts to OpenAI Skills schema
✅ Validates skill structure
✅ Interactive prompt builder
✅ Batch conversion for multiple files

## Limits

- Basic converter, enterprise features later
- No multi-file skill support yet

## Next Steps

- Add skill testing
- Add publishing helpers
- Support skill marketplace integration

---
*Created: 2026-03-08*
*Updated: 2026-03-08 - Added batch conversion*
