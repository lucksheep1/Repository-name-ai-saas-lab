#!/usr/bin/env python3
"""
Site Tracker - Minimal opportunity tracking with watchlist and quality tracking.

Phase 2 Features:
- Minimal watchlist (rule-based)
- Source quality tracking
"""

import argparse
import json
import re
import sqlite3
import ssl
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Config
DB_PATH = Path(__file__).parent / "tracker.db"
DEFAULT_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; SiteTracker/1.0)"

# Watchlist rules (simple)
HIGH_SIGNAL_SOURCES = ["GitHub Trending (Python)", "OpenAlternative"]
USEFUL_KEYWORDS = ["ai", "agent", "llm", "gpt", "chatbot", "memory", "mcp", "tool", "api", "dev", "code"]
RECENT_THRESHOLD_HOURS = 24


class TrackerDB:
    """SQLite persistence with dedup, noise filtering, watchlist, quality tracking."""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        
        # Opportunities table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT,
                category TEXT,
                discovered_at TEXT NOT NULL,
                first_seen_at TEXT,
                last_seen_at TEXT,
                appearance_count INTEGER DEFAULT 1,
                raw_data TEXT
            )
        """)
        
        # Runs table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                items_found INTEGER DEFAULT 0,
                items_saved INTEGER DEFAULT 0,
                error TEXT
            )
        """)
        
        # Source quality tracking
        conn.execute("""
            CREATE TABLE IF NOT EXISTS source_quality (
                source TEXT PRIMARY KEY,
                success_count INTEGER DEFAULT 0,
                useful_count INTEGER DEFAULT 0,
                noisy_count INTEGER DEFAULT 0,
                blocked_count INTEGER DEFAULT 0,
                last_success_at TEXT,
                last_run_at TEXT
            )
        """)
        
        # Watchlist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id INTEGER,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                reason TEXT NOT NULL,
                flagged_at TEXT NOT NULL,
                FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_opportunities(self, source: str, items: List[Dict], enable_dedup: bool = True):
        conn = sqlite3.connect(self.db_path)
        now = datetime.utcnow().isoformat()
        
        # Start run
        cursor = conn.execute(
            "INSERT INTO runs (source, started_at) VALUES (?, ?)",
            (source, now)
        )
        run_id = cursor.lastrowid
        
        saved_count = 0
        noisy_count = 0
        
        for item in items:
            # Skip noise
            if self._is_noise(item):
                noisy_count += 1
                continue
            
            url = item.get("url", "")
            title = item.get("title", "")
            
            # URL dedup
            if enable_dedup and url and url.startswith("http"):
                existing = conn.execute(
                    "SELECT id, appearance_count FROM opportunities WHERE url = ?",
                    (url,)
                ).fetchone()
                
                if existing:
                    conn.execute("""
                        UPDATE opportunities 
                        SET last_seen_at = ?, appearance_count = appearance_count + 1
                        WHERE id = ?
                    """, (now, existing[0]))
                    continue
            
            # Title dedup
            if enable_dedup and title:
                existing = conn.execute(
                    "SELECT id FROM opportunities WHERE LOWER(title) = LOWER(?)",
                    (title,)
                ).fetchone()
                
                if existing:
                    conn.execute("""
                        UPDATE opportunities 
                        SET last_seen_at = ?, appearance_count = appearance_count + 1
                        WHERE id = ?
                    """, (now, existing[0]))
                    continue
            
            # Insert new
            cursor = conn.execute("""
                INSERT INTO opportunities 
                (source, title, url, description, category, discovered_at, first_seen_at, last_seen_at, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source, title, url,
                item.get("description", ""),
                item.get("category", ""),
                now, now, now,
                json.dumps(item)
            ))
            opp_id = cursor.lastrowid
            
            # Check watchlist
            watchlist_reason = self._check_watchlist(item, source)
            if watchlist_reason:
                conn.execute("""
                    INSERT INTO watchlist (opportunity_id, source, title, url, reason, flagged_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (opp_id, source, title, url, watchlist_reason, now))
            
            saved_count += 1
        
        # Update run stats
        conn.execute("""
            UPDATE runs SET completed_at = ?, items_found = ?, items_saved = ? WHERE id = ?
        """, (now, len(items), saved_count, run_id))
        
        # Update source quality
        self._update_source_quality(conn, source, saved_count, noisy_count)
        
        conn.commit()
        conn.close()
        return saved_count
    
    def _update_source_quality(self, conn, source: str, saved: int, noisy: int):
        """Update source quality metrics."""
        now = datetime.utcnow().isoformat()
        
        existing = conn.execute(
            "SELECT success_count, noisy_count FROM source_quality WHERE source = ?",
            (source,)
        ).fetchone()
        
        if existing:
            conn.execute("""
                UPDATE source_quality 
                SET success_count = success_count + ?,
                    noisy_count = noisy_count + ?,
                    last_run_at = ?,
                    last_success_at = CASE WHEN ? > 0 THEN ? ELSE last_success_at END
                WHERE source = ?
            """, (saved, noisy, now, saved, now, source))
        else:
            conn.execute("""
                INSERT INTO source_quality (source, success_count, noisy_count, last_run_at, last_success_at)
                VALUES (?, ?, ?, ?, ?)
            """, (source, saved, noisy, now, now if saved > 0 else None))
    
    def _check_watchlist(self, item: Dict, source: str) -> Optional[str]:
        """Check if item matches watchlist rules. Returns reason if matched."""
        title = item.get("title", "").lower()
        url = item.get("url", "").lower()
        
        # 1. High-signal source
        if source in HIGH_SIGNAL_SOURCES:
            return f"high_signal_source:{source}"
        
        # 2. Useful keywords in title
        for kw in USEFUL_KEYWORDS:
            if kw in title:
                return f"keyword:{kw}"
        
        # 3. Useful keywords in URL
        for kw in USEFUL_KEYWORDS:
            if kw in url:
                return f"url_keyword:{kw}"
        
        return None
    
    def _normalize_title(self, title: str) -> str:
        return re.sub(r'[^a-z0-9]', '', title.lower())
    
    def _is_noise(self, item: Dict) -> bool:
        title = item.get("title", "")
        url = item.get("url", "")
        
        if len(title) < 3:
            return True
        
        noise_patterns = ["+ Launch", "+ New", "+ Add", "human", "Click", 
                         "Button", "Sign up", "Login", "Submit", "aria-", 
                         "crossOrigin", "data-"]
        
        for pattern in noise_patterns:
            if pattern.lower() in title.lower():
                return True
        
        if url and not url.startswith("http"):
            return True
        
        if "tally.so" in url:
            return True
        
        return False
    
    def get_recent(self, source: str = None, limit: int = 50) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        if source:
            rows = conn.execute("""
                SELECT title, url, description, category, discovered_at, source
                FROM opportunities WHERE source = ?
                ORDER BY discovered_at DESC LIMIT ?
            """, (source, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT title, url, description, category, discovered_at, source
                FROM opportunities
                ORDER BY discovered_at DESC LIMIT ?
            """, (limit,)).fetchall()
        conn.close()
        
        return [
            {"title": r[0], "url": r[1], "description": r[2], 
             "category": r[3], "discovered_at": r[4], "source": r[5]}
            for r in rows
        ]
    
    def get_watchlist(self, limit: int = 50) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("""
            SELECT w.source, o.title, o.url, w.reason, w.flagged_at, o.first_seen_at, o.last_seen_at, o.appearance_count
            FROM watchlist w
            JOIN opportunities o ON w.opportunity_id = o.id
            ORDER BY w.flagged_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        conn.close()
        
        return [
            {"source": r[0], "title": r[1], "url": r[2], "reason": r[3], 
             "flagged_at": r[4], "first_seen": r[5], "last_seen": r[6], "count": r[7]}
            for r in rows
        ]
    
    def get_source_quality(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute("""
            SELECT source, success_count, useful_count, noisy_count, blocked_count, last_success_at, last_run_at
            FROM source_quality
            ORDER BY success_count DESC
        """).fetchall()
        conn.close()
        
        return [
            {"source": r[0], "success": r[1], "useful": r[2], "noisy": r[3], 
             "blocked": r[4], "last_success": r[5], "last_run": r[6]}
            for r in rows
        ]


def fetch_page(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  Fetch error: {e}", file=sys.stderr)
        return None


# ==================== SITE HANDLERS ====================

class BaseSite:
    name: str = ""
    url: str = ""
    
    def fetch(self) -> Optional[str]:
        return fetch_page(self.url)
    
    def extract(self, html: str) -> List[Dict]:
        return []
    
    def run(self) -> List[Dict]:
        print(f"  Fetching {self.name}...")
        html = self.fetch()
        if not html:
            print(f"  Failed to fetch")
            return []
        
        items = self.extract(html)
        print(f"  Found {len(items)} items")
        return items


class GitHubTrending(BaseSite):
    name = "GitHub Trending (Python)"
    url = "https://api.github.com/search/repositories?q=created:>2024-01-01+language:python&sort=stars&order=desc&per_page=20"
    
    def fetch(self) -> Optional[str]:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(
            self.url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"  API error: {e}", file=sys.stderr)
            return None
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        if not html:
            return items
        
        try:
            data = json.loads(html)
            for repo in data.get("items", [])[:20]:
                items.append({
                    "title": repo.get("full_name", ""),
                    "url": repo.get("html_url", ""),
                    "description": (repo.get("description") or "")[:150],
                    "category": "code"
                })
        except Exception as e:
            print(f"  Parse error: {e}", file=sys.stderr)
        
        return items


class HackerNewsShow(BaseSite):
    name = "Hacker News"
    url = "https://news.ycombinator.com/"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*class="titlelink"[^>]*>([^<]+)</a>'
        for url, title in re.findall(pattern, html)[:15]:
            items.append({"title": title.strip(), "url": url, "description": "Hacker News", "category": "startup"})
        return items


class BetaListSite(BaseSite):
    name = "BetaList"
    url = "https://betalist.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(/startup/[^"]+)"[^>]*>([^<]+)</a>'
        for path, title in re.findall(pattern, html)[:15]:
            items.append({"title": title.strip(), "url": f"https://betalist.com{path}", "description": "BetaList", "category": "startup"})
        return items


class ExplodingTopics(BaseSite):
    name = "Exploding Topics"
    url = "https://explodingtopics.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://explodingtopics\.com/[^"]+)"[^>]*>([^<]+)</a>'
        seen = set()
        for url, title in re.findall(pattern, html)[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({"title": title.strip(), "url": url, "description": "Exploding Topics", "category": "trend"})
        return items


class FutureTools(BaseSite):
    name = "FutureTools"
    url = "https://futuretools.io"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*class="[^"]*tool[^"]*"[^>]*>([^<]+)</a>'
        seen = set()
        for url, title in re.findall(pattern, html)[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({"title": title.strip(), "url": url, "description": "AI Tool", "category": "tool"})
        return items


class AlternativeTo(BaseSite):
    name = "AlternativeTo"
    url = "https://alternativeto.net"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://alternativeto\.net/[^"]+)"[^>]*>([^<]+)</a>'
        seen = set()
        for url, title in re.findall(pattern, html)[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({"title": title.strip(), "url": url, "description": "Alternative", "category": "tool"})
        return items


class TinyStartups(BaseSite):
    name = "Tiny Startups"
    url = "https://www.tinystartups.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>'
        seen = set()
        for url, title in re.findall(pattern, html)[:15]:
            title = title.strip()
            if title and len(title) > 5 and title not in seen:
                seen.add(title)
                items.append({"title": title, "url": url, "description": "Tiny Startups", "category": "startup"})
        return items


class OpenAlternative(BaseSite):
    name = "OpenAlternative"
    url = "https://openalternative.co"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>'
        seen = set()
        for url, title in re.findall(pattern, html)[:15]:
            title = title.strip()
            if title and len(title) > 3 and title not in seen:
                seen.add(title)
                items.append({"title": title, "url": url, "description": "Open Alternative", "category": "tool"})
        return items


TRACKERS = {
    "github": GitHubTrending,
    "hn": HackerNewsShow,
    "betalist": BetaListSite,
    "exploding": ExplodingTopics,
    "futuretools": FutureTools,
    "alternativeto": AlternativeTo,
    "tinystartups": TinyStartups,
    "openalternative": OpenAlternative,
}


def run_tracker(name: str, db: TrackerDB) -> int:
    if name not in TRACKERS:
        print(f"Unknown: {name}")
        return 1
    
    tracker = TRACKERS[name]()
    items = tracker.run()
    
    if items:
        count = db.save_opportunities(tracker.name, items)
        print(f"  Saved {count} items")
    
    return 0


def run_all(db: TrackerDB) -> int:
    print(f"Running {len(TRACKERS)} trackers...\n")
    
    total = 0
    for name, cls in TRACKERS.items():
        print(f"[{name}]")
        tracker = cls()
        items = tracker.run()
        if items:
            count = db.save_opportunities(tracker.name, items)
            print(f"  -> Saved {count}")
            total += count
        print()
    
    print(f"Total: {total} opportunities saved")
    return 0


def show_watchlist(db: TrackerDB, limit: int = 20):
    items = db.get_watchlist(limit)
    
    if not items:
        print("No watchlist items.")
        return
    
    print(f"Watchlist ({len(items)} items):\n")
    for item in items:
        print(f"[{item['source']}] {item['title']}")
        print(f"  Reason: {item['reason']}")
        print(f"  URL: {item['url']}")
        print(f"  Seen: {item['count']}x (first: {item['first_seen'][:19]}, last: {item['last_seen'][:19]})")
        print()


def show_quality(db: TrackerDB):
    sources = db.get_source_quality()
    
    if not sources:
        print("No quality data yet.")
        return
    
    print("Source Quality:\n")
    print(f"{'Source':<25} {'Success':>8} {'Noisy':>8} {'Last Success':>20}")
    print("-" * 70)
    for s in sources:
        last = s['last_success'][:19] if s['last_success'] else "never"
        print(f"{s['source']:<25} {s['success']:>8} {s['noisy']:>8} {last:>20}")


def main():
    parser = argparse.ArgumentParser(description="Site Tracker Phase 2")
    parser.add_argument("command", nargs="?", default="list",
                        choices=["run", "list", "recent", "watchlist", "quality"])
    parser.add_argument("site", nargs="?", default=None)
    parser.add_argument("--limit", type=int, default=20)
    
    args = parser.parse_args()
    db = TrackerDB()
    
    if args.command == "list":
        print("Available trackers:")
        for name, cls in TRACKERS.items():
            print(f"  {name:15} - {cls.name}")
    
    elif args.command == "run":
        if args.site:
            sys.exit(run_tracker(args.site, db))
        else:
            sys.exit(run_all(db))
    
    elif args.command == "recent":
        items = db.get_recent(args.site, args.limit)
        for item in items:
            print(f"[{item['source']}] {item['title']} - {item['url']}")
    
    elif args.command == "watchlist":
        show_watchlist(db, args.limit)
    
    elif args.command == "quality":
        show_quality(db)


if __name__ == "__main__":
    main()