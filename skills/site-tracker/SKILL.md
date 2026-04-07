---
name: site-tracker
description: |
  Tracks developer-tool and AI opportunity signals from curated web sources.
  Activate when user mentions "track opportunities", "scan sources", "run tracker",
  "watchlist", or "opportunity discovery".
---

# Site Tracker Skill

Tracks developer-tool and AI startup opportunities by crawling curated web sources,
de-duplicating results, and maintaining a SQLite-backed watchlist with source-quality metrics.

## Target

**Goal:** Continuously discover emerging AI/developer-tool projects and signals from the open web,
without requiring API keys or login. Feed the watchlist for further analysis or outreach.

---

## How to Run

```bash
cd /root/.openclaw/workspace/projects/site-tracker
./run.sh           # run all active trackers + generate report
python3 tracker.py run [hn|github|...]   # run single tracker
python3 tracker.py recent --limit 20      # view recent items
python3 tracker.py watchlist             # view watchlist
python3 tracker.py quality               # view source quality stats
```

---

## Source Status

### Active Sources

| Key | Name | Status | Notes |
|-----|------|--------|-------|
| `github` | GitHub Trending (Python) | ✅ Primary | Pulls Top 20 Python repos. High dedup hit rate. Stable. |
| `hn` | Hacker News (grouped) | ✅ Active | Sub-classified into Discussion / Show HN / Launch HN. Quality filtered. |
| `openalternative` | OpenAlternative | ✅ Stable | AI tool alternatives. Good signal/noise ratio. |

### Inactive / Retired Sources

| Key | Name | Status | Reason |
|-----|------|--------|--------|
| `tinystartups` | Tiny Startups | 🚫 Excluded | 210 noise / 2 success. Basic regex too loose. |
| `betalist` | BetaList | ❌ Failing | Returns 0 items. Site likely blocks or changed structure. |
| `exploding` | Exploding Topics | ❌ Failing | Returns 0 items. |
| `futuretools` | FutureTools | ❌ Failing | Returns 0 items. |
| `alternativeto` | AlternativeTo | ❌ Failing | Returns 0 items. |

---

## What Is Tracked

- **GitHub Trending repos** in Python language
- **Hacker News submissions** filtered by:
  - `Launch HN` / `Show HN` → always included (opportunity signal)
  - `Discussion` → included only if title contains quality keywords (`tool`, `agent`, `open-source`, `api`, `llm`, etc.)
- **OpenAlternative AI tool listings**

**Watchlist rules:**
- High-signal sources → auto-watchlist (`high_signal_source:GitHub Trending (Python)`)
- HN sub-sources → tagged by sub-type (`source:Hacker News (Discussion)`)
- Keyword matches in title or URL → tagged (`keyword:agent`, `url_keyword:dev`)

---

## What Is NOT In Scope

- 🔴 **Login / auth-gated sources** (HN, Product Hunt with accounts)
- 🔴 **Comment scraping** ( HN replies, Reddit threads)
- 🔴 **Complex NLP / LLM scoring** of opportunity quality
- 🔴 **Multi-source scoring models** or ranking
- 🔴 **Real-time streaming** (this is a pull-based batch tracker)
- 🔴 **API-based sources** requiring keys (serpapi, Twitter API, etc.)

---

## Current Limitations

1. **GitHub Trending is a "stable pool"** — Top 20 Python repos repeat daily. Watchlist expansion depends on new entrants, not frequency.
2. **HN deduplication is aggressive** — items already in DB (by URL) won't re-appear, even if the item is still climbing on HN front page.
3. **No sub-source granularity for GitHub** — only one source name for all GitHub items.
4. **No scheduling** is managed by this skill. Use external cron to invoke `run.sh`.

---

## Upgrade Checklist (future, not now)

### P0 — Fix gaps
- [ ] Fix HN to also pull from `https://news.ycombinator.com/newest` (newest first) in addition to front page
- [ ] Separate GitHub sub-source by programming language (not just Python)
- [ ] Add HN Ask HN / Job HN classification (Ask HN = community signal, Job HN = talent market signal)

### P1 — Improve signal quality
- [ ] Switch HN to RSS feed (`https://hnrss.org/frontpage`) for cleaner extraction than HTML regex
- [ ] Add `high_signal_source:Hacker News (Launch HN)` to HIGH_SIGNAL_SOURCES so Launch HN auto-enters watchlist
- [ ] Track "days on watchlist" to identify stale items

### P2 — Expand reach
- [ ] Replace failing sources (BetaList → Product Hunt via public RSS)
- [ ] Add `https://github.com/trending` multi-language scan
- [ ] Add keyword alerting (new item matching specific keywords → notify)

### P3 — Architecture
- [ ] Extract tracker classes into separate files for maintainability
- [ ] Add per-source timeout config (currently hardcoded 15s)
- [ ] Replace `datetime.utcnow()` deprecation with `datetime.now(datetime.UTC)`

---

## Database Schema

```
opportunities   — title, url, source, description, category, appearance_count, first_seen_at, last_seen_at
runs            — source, started_at, completed_at, items_found, items_saved, error
source_quality  — source, success_count, noisy_count, last_success_at
watchlist       — source, title, url, reason, flagged_at
```

DB location: `/root/.openclaw/workspace/projects/site-tracker/tracker.db`
