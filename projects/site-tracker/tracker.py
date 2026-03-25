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
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error
import ssl

# Config
DB_PATH = Path(__file__).parent / "tracker.db"
DEFAULT_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; SiteTracker/1.0)"

class TrackerDB:
    """Simple SQLite persistence for tracked opportunities."""
    
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
    
    def save_opportunities(self, source: str, items: List[Dict]):
        conn = sqlite3.connect(self.db_path)
        now = datetime.utcnow().isoformat()
        
        run_id = None
        # Start run
        cursor = conn.execute(
            "INSERT INTO runs (source, started_at) VALUES (?, ?)",
            (source, now)
        )
        run_id = cursor.lastrowid
        
        for item in items:
            conn.execute("""
                INSERT INTO opportunities 
                (source, title, url, description, category, discovered_at, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                source,
                item.get("title", ""),
                item.get("url", ""),
                item.get("description", ""),
                item.get("category", ""),
                now,
                json.dumps(item)
            ))
        
        conn.execute(
            "UPDATE runs SET completed_at = ?, items_found = ? WHERE id = ?",
            (now, len(items), run_id)
        )
        conn.commit()
        conn.close()
        return len(items)
    
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
        """Override in subclass."""
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
    """GitHub Trending - Python repos."""
    name = "GitHub Trending (Python)"
    url = "https://github.com/trending/python?since=daily"
    
    def extract(self, html: str) -> List[Dict]:
        items = []
        
        # Simple regex-based extraction (no external deps)
        import re
        
        # Find repo links: <a href="/owner/repo">...
        repo_pattern = r'<a\s+href="(/[^/]+/[^"]+)"[^>]*>.*?</a>\s*</article>'
        
        # Simpler: find all repo links in the page
        link_pattern = r'href="(/[^/]+/[^/]+/[^"]+)"'
        matches = re.findall(link_pattern, html)
        
        seen = set()
        for match in matches[:20]:  # Limit to 20
            if match.startswith('/') and '/' in match[1:]:
                parts = match.strip('/').split('/')
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    full_name = f"{owner}/{repo}"
                    if full_name not in seen and '?' not in match:
                        seen.add(full_name)
                        items.append({
                            "title": full_name,
                            "url": f"https://github.com{match}",
                            "description": "GitHub Trending Python repo",
                            "category": "code"
                        })
        
        return items


class HackerNewsShow(BaseSite):
    """Hacker News Show HN."""
    name = "Hacker News Show"
    url = "https://news.ycombinator.com/"
    
    def extract(self, html: str) -> List[Dict]:
        import re
        items = []
        
        # Find story links: <a href="url" class="titlelink">Title</a>
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
        import re
        items = []
        
        # Find startup entries
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
        import re
        items = []
        
        # Look for topic links
        pattern = r'<a[^>]*href="(https?://explodingtopics\.com/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for url, title in matches[:15]:
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
        import re
        items = []
        
        # Find tool cards
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*class="[^"]*tool[^"]*"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for url, title in matches[:15]:
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
        import re
        items = []
        
        # Find alternatives
        pattern = r'<a[^>]*href="(https?://alternativeto\.net/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for url, title in matches[:15]:
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
        import re
        items = []
        
        # Find startup links
        pattern = r'<a[^>]*href="(https?://[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for url, title in matches[:15]:
            title = title.strip()
            if title and title not in seen:
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
        import re
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


# Registry of available trackers
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
    """Run a single tracker."""
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
    """Run all trackers."""
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
    
    print(f"Total: {total} opportunities found")
    return 0


def list_sites():
    """List available sites."""
    print("Available trackers:")
    for name, cls in TRACKERS.items():
        print(f"  {name:15} - {cls.name}")
    print()


def show_recent(db: TrackerDB, source: str = None, limit: int = 20):
    """Show recent opportunities."""
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
            print(f"  {item['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Site Tracker - Monitor opportunity websites")
    parser.add_argument("command", nargs="?", default="list",
                        choices=["run", "list", "recent"])
    parser.add_argument("site", nargs="?", help="Site name for run/recent")
    parser.add_argument("--limit", type=int, default=20, help="Limit for recent command")
    
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