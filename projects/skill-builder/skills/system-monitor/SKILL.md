---
name: system-monitor
description: Monitor system resources and receive alerts for CPU, memory, disk, and network usage. Set threshold-based alerts. Use when: checking system health, investigating high resource usage, or reviewing process lists.
---

# System Monitor

## When to Use

Use this skill when the user mentions: monitor, cpu, memory, disk, process, alert, resource, usage, system health.


## SENSITIVE DATA

System monitoring shows resource usage. Process lists may reveal software installed. No personal user data exposed.

## Session Start

Run `top -bn1 | head -20` for quick process overview. Run `df -h` for disk, `free -m` for memory.

## Commands

- `status` — CPU, memory, disk overview
- `processes [--top N]` — top N processes by CPU/memory
- `disk` — disk usage for all mounts
- `network` — active network connections
- `alert <metric> <threshold>` — set up alert

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
