#!/usr/bin/env python3
"""
Site Tracker - Minimal website opportunity tracking layer.

Usage:
    python tracker.py --help
    python tracker.py run          # Run all trackers
    python tracker.py run github   # Run specific tracker
    python tracker.py list         # List available sites
"""

import argparse
import json
import os
import sys
import sqlite3
import time
import ssl
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error

# Config
DB_PATH = Path(__file__).parent / "tracker.db"
DEFAULT_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; SiteTracker/1.0)"


class TrackerDB:
    """Simple SQLite persistence with dedup and noise filtering."""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                items_found INTEGER DEFAULT 0,
                error TEXT
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
        for item in items:
            # Skip noise
            if self._is_noise(item):
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
            
            # Title dedup (normalized)
            if enable_dedup and title:
                norm_title = self._normalize_title(title)
                if norm_title:
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
            conn.execute("""
                INSERT INTO opportunities 
                (source, title, url, description, category, discovered_at, first_seen_at, last_seen_at, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source,
                title,
                url,
                item.get("description", ""),
                item.get("category", ""),
                now,
                now,
                now,
                json.dumps(item)
            ))
            saved_count += 1
        
        conn.execute(
            "UPDATE runs SET completed_at = ?, items_found = ? WHERE id = ?",
            (now, saved_count, run_id)
        )
        conn.commit()
        conn.close()
        return saved_count
    
    def _normalize_title(self, title: str) -> str:
        """Normalize title for dedup."""
        return re.sub(r'[^a-z0-9]', '', title.lower())
    
    def _is_noise(self, item: Dict) -> bool:
        """Filter obvious noise."""
        title = item.get("title", "")
        url = item.get("url", "")
        
        if len(title) < 3:
            return True
        
        noise_patterns = [
            "+ Launch", "+ New", "+ Add", "human", "Click", 
            "Button", "Sign up", "Login", "Submit", "aria-", 
            "crossOrigin", "data-"
        ]
        
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


def fetch_page(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
    """Simple HTTP fetch - no JS rendering."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  Fetch error: {e}", file=sys.stderr)
        return None


# ==================== SITE HANDLERS ====================

class BaseSite:
    """Base class for site trackers."""
    
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
    """GitHub Trending - Python repos via API."""
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
    """Hacker News."""
    name = "Hacker News"
    url = "https://news.ycombinator.com/"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*class="titlelink"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for url, title in matches[:15]:
            items.append({
                "title": title.strip(),
                "url": url,
                "description": "Hacker News",
                "category": "startup"
            })
        
        return items


class BetaListSite(BaseSite):
    """BetaList."""
    name = "BetaList"
    url = "https://betalist.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(/startup/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for path, title in matches[:15]:
            items.append({
                "title": title.strip(),
                "url": f"https://betalist.com{path}",
                "description": "BetaList startup",
                "category": "startup"
            })
        
        return items


class ExplodingTopics(BaseSite):
    """Exploding Topics."""
    name = "Exploding Topics"
    url = "https://explodingtopics.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://explodingtopics\.com/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({
                    "title": title.strip(),
                    "url": url,
                    "description": "Exploding Topics",
                    "category": "trend"
                })
        
        return items


class FutureTools(BaseSite):
    """FutureTools."""
    name = "FutureTools"
    url = "https://futuretools.io"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*class="[^"]*tool[^"]*"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({
                    "title": title.strip(),
                    "url": url,
                    "description": "AI Tool",
                    "category": "tool"
                })
        
        return items


class AlternativeTo(BaseSite):
    """AlternativeTo."""
    name = "AlternativeTo"
    url = "https://alternativeto.net"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://alternativeto\.net/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            if title.strip() not in seen:
                seen.add(title.strip())
                items.append({
                    "title": title.strip(),
                    "url": url,
                    "description": "Alternative software",
                    "category": "tool"
                })
        
        return items


class TinyStartups(BaseSite):
    """Tiny Startups."""
    name = "Tiny Startups"
    url = "https://www.tinystartups.com"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            title = title.strip()
            if title and len(title) > 5 and title not in seen:
                seen.add(title)
                items.append({
                    "title": title,
                    "url": url,
                    "description": "Tiny Startups",
                    "category": "startup"
                })
        
        return items


class OpenAlternative(BaseSite):
    """OpenAlternative."""
    name = "OpenAlternative"
    url = "https://openalternative.co"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            title = title.strip()
            if title and len(title) > 3 and title not in seen:
                seen.add(title)
                items.append({
                    "title": title,
                    "url": url,
                    "description": "Open Alternative",
                    "category": "tool"
                })
        
        return items


# Registry
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
        print(f"Unknown tracker: {name}")
        print(f"Available: {', '.join(TRACKERS.keys())}")
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


def list_sites():
    print("Available trackers:")
    for name, cls in TRACKERS.items():
        print(f"  {name:15} - {cls.name}")
    print()


def show_recent(db: TrackerDB, source: str = None, limit: int = 20):
    items = db.get_recent(source, limit)
    
    if not items:
        print("No opportunities found.")
        return
    
    print(f"Recent {len(items)} opportunities:\n")
    for item in items:
        print(f"[{item['source']}]")
        print(f"  {item['title']}")
        print(f"  {item['url']}")
        if item.get('description'):
            print(f"  {item['description'][:80]}...")
        print()


def main():
    parser = argparse.ArgumentParser(description="Site Tracker")
    parser.add_argument("command", nargs="?", default="list",
                        choices=["run", "list", "recent"])
    parser.add_argument("site", nargs="?", help="Site name")
    parser.add_argument("--limit", type=int, default=20)
    
    args = parser.parse_args()
    db = TrackerDB()
    
    if args.command == "list":
        list_sites()
    elif args.command == "run":
        if args.site:
            sys.exit(run_tracker(args.site, db))
        else:
            sys.exit(run_all(db))
    elif args.command == "recent":
        show_recent(db, args.site, args.limit)


if __name__ == "__main__":
    main()