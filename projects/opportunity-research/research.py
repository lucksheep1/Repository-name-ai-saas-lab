#!/usr/bin/env python3
"""
Opportunity Research - Signal-driven research executor.
Selects strongest signal from site-tracker watchlist and generates a formal research memo.
"""

import sqlite3
import sys
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "site-tracker" / "tracker.db"
WATCHLIST_LIMIT = 20


def get_candidates():
    """Fetch candidates from watchlist, prioritizing multi-source then single persistent."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT
            w.source, w.title, w.url, w.reason, w.flagged_at,
            o.appearance_count, o.first_seen_at, o.last_seen_at,
            o.description, o.category
        FROM watchlist w
        JOIN opportunities o ON w.opportunity_id = o.id
        ORDER BY o.appearance_count DESC, w.flagged_at DESC
        LIMIT ?
    """, (WATCHLIST_LIMIT,)).fetchall()
    conn.close()
    return rows


def score_candidate(row):
    """Score a candidate. Returns (score, signal_type)."""
    source, title, url, reason, flagged_at, appearance_count, first_seen, last_seen, description, category = row

    # Multi-source detection: group by title across sources
    conn = sqlite3.connect(DB_PATH)
    same_title = conn.execute("""
        SELECT COUNT(DISTINCT source) FROM opportunities
        WHERE LOWER(title) = LOWER(?)
    """, (title,)).fetchone()[0]
    conn.close()

    score = 0
    signal_type = "single_source_persistent"

    if same_title >= 2:
        score += 100
        signal_type = "multi_source_resonance"
    else:
        score += 10

    score += appearance_count

    # Bonus for high-signal source keywords
    if "high_signal_source" in (reason or ""):
        score += 20
    if "Launch HN" in source or "Show HN" in source:
        score += 15
    if "Hacker News" in source:
        score += 10

    return score, signal_type


def select_candidate(rows):
    """Select the strongest candidate based on scoring."""
    scored = []
    for row in rows:
        score, sig_type = score_candidate(row)
        scored.append((score, sig_type, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[0]
    return top[1], top[2]  # signal_type, row


def build_watchlist_context(rows):
    """Build top-5 context for 'why this one' narrative."""
    top5 = rows[:5]
    lines = []
    for i, r in enumerate(top5, 1):
        source, title, url, reason, flagged, cnt, first, last, desc, cat = r
        lines.append(f"{i}. x{cnt} [{source}] {title[:55]}")
    return "\n".join(lines)


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[opportunity-research] Starting at {now}")

    rows = get_candidates()
    if not rows:
        print("No candidates in watchlist. Exiting.")
        sys.exit(0)

    signal_type, top_row = select_candidate(rows)
    source, title, url, reason, flagged_at, appearance_count, first_seen, last_seen, description, category = top_row

    print(f"Selected: {title}")
    print(f"  signal_type={signal_type}")
    print(f"  source={source}, x{appearance_count}")
    print(f"  url={url}")

    # Output structured data for downstream processing
    output = {
        "run_at": now,
        "signal_type": signal_type,
        "signal_score": appearance_count,
        "source": source,
        "title": title,
        "url": url,
        "reason": reason,
        "appearance_count": appearance_count,
        "flagged_at": flagged_at,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "description": description or "",
        "category": category or "",
        "watchlist_top5_context": build_watchlist_context(rows),
    }

    # Write to temp file for downstream to consume
    out_path = Path(__file__).parent / ".last_research.json"
    with open(out_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[WATCHLIST_TOP5]")
    print(build_watchlist_context(rows))
    print(f"\n[RESEARCH_INPUT_JSON_SAVED]")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
