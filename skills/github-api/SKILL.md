---
name: github-api
description: |
  GitHub API integration via the Maton gateway. Use this skill for HTTP/API-style GitHub access,
  managed OAuth connections, and JSON responses. This skill is distinct from github-cli, which uses gh.
compatibility: Requires network access and a valid Maton API key
metadata:
  author: maton
  version: "1.1"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# GitHub API

Use this skill when the task should go through the Maton GitHub gateway and return structured API responses.
Do not confuse it with github-cli, which shells out to gh.

## Required Dependency

- MATON_API_KEY
- Network access to gateway.maton.ai and ctrl.maton.ai

## Current Status

- MATON_API_KEY: unconfigured in the current server shell
- Fallback: none

## Quick Start

```bash
python <<'PY'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/github/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
PY
```

## Base URL

```
https://gateway.maton.ai/github/{native-api-path}
```

Replace `{native-api-path}` with the actual GitHub API endpoint path. The gateway proxies requests to `api.github.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

## Connection Management

Manage your GitHub OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'PY'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=github&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
PY
```

### Create Connection

```bash
python <<'PY'
import urllib.request, os, json
data = json.dumps({'app': 'github'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
PY
```

### Specify a Connection

If multiple GitHub connections exist, add the Maton-Connection header.

```bash
python <<'PY'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/github/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'your-connection-id')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
PY
```
