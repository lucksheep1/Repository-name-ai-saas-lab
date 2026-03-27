---
name: linux-server-ops
description: Manage Linux servers via SSH for AI agents. Deploy websites, configure databases, set up SSL certificates, manage Docker containers, monitor resources, and configure Nginx. Like a BaoTa/1Panel but AI-driven. Use when: deploying services, checking server status, restarting services, configuring SSL, or managing Docker on remote servers.
---

# Linux Server Ops

## When to Use

Use this skill when the user mentions: deploy, server, ssh, linux, ssl, nginx, docker, database, restart, monitor, web server, devops, hosting.


## SENSITIVE DATA

CRITICAL: Never display server IPs, SSH keys, or passwords. Always use server ID (e.g., 'prod-web') instead of IP. Mask all secrets in output.

## Session Start

Check for .server/servers.json and .server/snapshots/. Load existing server context before making changes.

## Commands

- `status <server-id>` — check server resources
- `deploy <server-id> <service>` — deploy service
- `ssl <domain>` — provision SSL certificate
- `docker ps <server-id>` — list containers
- `restart <service>` — restart a service

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
