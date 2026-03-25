# Site Tracker - Minimal Website Opportunity Tracking

A lightweight, headless website tracker that monitors public startup/opportunity sites.

## Quick Start

```bash
cd projects/site-tracker

# List available trackers
python tracker.py list

# Run all trackers
python tracker.py run

# Run specific tracker
python tracker.py run github

# Show recent results
python tracker.py recent
```

## Available Trackers

| Key | Site | Description |
|-----|------|-------------|
| github | GitHub Trending | Python repos |
| hn | Hacker News | Top stories |
| betalist | BetaList | Upcoming startups |
| exploding | Exploding Topics | Trending topics |
| futuretools | FutureTools | AI tools |
| alternativeto | AlternativeTo | Software alternatives |
| tinystartups | Tiny Startups | Small startup deals |
| openalternative | OpenAlternative | Open source alternatives |

## Output

Results are saved to `tracker.db` (SQLite):

```bash
# View recent opportunities
python tracker.py recent --limit 20

# View specific source
python tracker.py recent github
```

## Run Scheduling

Add to cron for periodic execution:

```bash
# Run every hour
0 * * * * cd /path/to/site-tracker && python tracker.py run >> /var/log/tracker.log 2>&1
```

## Phase 2 (Deferred)

- Login/session-heavy sites
- JavaScript rendering (playwright/selenium)
- Better extraction logic
- Ranking algorithm

## Dependencies

- Python 3.8+
- Standard library only (urllib, sqlite3, re)

---
*Created: 2026-03-25*