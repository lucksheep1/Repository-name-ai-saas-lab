---
name: web-scraper
description: Extract structured data from websites. Fetch and parse HTML into readable text, take screenshots. Use when: extracting data from webpages, monitoring pages for changes, or capturing content from URLs.
---

# Web Scraper

## When to Use

Use this skill when the user mentions: scrape, extract, fetch content, parse html, web page, screenshot, crawl.


## SENSITIVE DATA

Web scraping may be subject to robots.txt and Terms of Service. Always check before scraping. No credentials needed for public pages.

## Session Start

Use web_fetch for simple content extraction. Use browser tool for JavaScript-rendered pages or interactive content.

## Commands

- `fetch <url>` — extract readable text from URL
- `screenshot <url>` — capture page screenshot
- `extract <url> --selector <css>` — extract specific DOM elements

## Quality Standards

- Always verify destructive operations before executing
- Report progress clearly during long-running tasks
- Mask all sensitive data in output
- Maintain context between commands in a session
