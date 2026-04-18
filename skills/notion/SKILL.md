---
name: notion
description: Notion API for creating and managing pages, databases, and blocks.
homepage: https://developers.notion.com
metadata: {"clawdbot":{"emoji":"📝"}}
---

# notion

## purpose

Operate Notion pages, data sources, and blocks through the Notion API.

## when_to_use

- When the user explicitly wants to read or write Notion content
- When the target system is a Notion page or data source

## do_not_use_for

- Tasks that do not target Notion
- Cases where local markdown or another document system is the actual destination
- Situations where API access is required but local credential state is unknown and cannot be assumed safe

## inputs

- notion page id or data source id
- requested API operation
- content payload or query payload
- local API credential file

## outputs

- API request result
- target page or data source identifier
- failure reason if the operation cannot proceed

## required_dependencies

- Notion API key file at `~/.config/notion/api_key`
- network access to `api.notion.com`
- valid `Notion-Version` header

## current_status

- `/root/.config/notion/api_key`: present
- `/home/ubuntu/.config/notion/api_key`: present
- API/network verification: not performed in this batch
- effective status: configured but unverified

## fallback

- If the API key file is missing or unreadable: stop and report missing credential
- If network/API access is unavailable: stop and report unverified or failed access
- No local offline fallback is defined by this skill

## Setup

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it:
```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```
4. Share target pages/databases with your integration

## API Basics

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

The `Notion-Version` header is required. This skill uses `2025-09-03`.

## Common Operations

Search, get pages, get blocks, create pages, query data sources, create data sources, update pages, and append blocks using the official endpoints documented below.
