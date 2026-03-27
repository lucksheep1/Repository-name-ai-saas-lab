#!/usr/bin/env python3
"""
web-search: Web search and page fetch CLI tool.

Uses Brave Search API for web search.
Part of the agent-native toolkit.

Usage:
    python cli.py search "what is agent-memory"
    python cli.py fetch "https://github.com/michael-ltm/linux-server-skill"
    python cli.py summarize "https://example.com/article"
    python cli.py doctor  # Check API configuration
"""

import argparse
import sys
import os
import re
import json as json_mod


def get_api_key():
    """Get Brave Search API key from environment."""
    return os.environ.get("BRAVE_SEARCH_KEY") or os.environ.get("BRAVE_API_KEY")


def do_search(query, count=5, freshness=None):
    """Perform a web search using Brave Search API."""
    api_key = get_api_key()
    if not api_key:
        print("❌ Brave Search API key not found.")
        print("   Set BRAVE_SEARCH_KEY or BRAVE_API_KEY environment variable.")
        print("   Get your free key at: https://brave.com/search/api/")
        return None

    try:
        import requests
        params = {"q": query, "count": min(count, 10)}
        if freshness:
            params["freshness"] = freshness

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        }
        resp = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params=params,
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        results = data.get("web", {}).get("results", [])
        print(f"\n🔍 Search: {query}\n")
        for i, r in enumerate(results[:count], 1):
            title = r.get("title", "")
            url_r = r.get("url", "")
            desc = r.get("description", "")
            age = r.get("age", "")
            print(f"  {i}. {title}")
            print(f"     {url_r}")
            if desc:
                print(f"     {desc[:150]}...")
            if age:
                print(f"     ({age})")
            print()
        return results

    except ImportError:
        print("❌ requests library not available")
        return None
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return None


def strip_html(html):
    """Remove HTML tags from text."""
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def do_fetch(url):
    """Fetch and display readable content from a URL."""
    try:
        import requests
        req_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; ai-agent/1.0)"
        }
        resp = requests.get(url, headers=req_headers, timeout=15)
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")

        if "html" in content_type.lower() or "<html" in resp.text[:200].lower():
            text = strip_html(resp.text)
        else:
            text = resp.text

        preview = text[:2000]
        print(f"\n📄 Fetch: {url}\n")
        print(f"  [{len(text)} total chars — showing first 2000]\n")
        print(preview)
        if len(text) > 2000:
            print(f"\n  ... [{len(text) - 2000} more chars]")
        return text

    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        return None


def do_summarize(url):
    """Summarize a URL using extractive summarization."""
    text = do_fetch(url)
    if not text:
        return

    # Simple extractive summarization: score sentences by position and keyword density
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    sentences = sentences[:50]

    # Score sentences
    scored = []
    for i, s in enumerate(sentences):
        # First sentences and longer sentences score higher
        pos_score = max(0, 10 - i // 5)
        len_score = min(len(s) // 50, 10)
        score = pos_score + len_score
        scored.append((score, s))

    scored.sort(key=lambda x: -x[0])
    top = scored[:5]

    print(f"\n📝 Summary ({len(top)} key sentences):\n")
    for score, s in top:
        print(f"  • {s[:200]}")
        print()


def cmd_doctor(args):
    """Check Brave Search API status."""
    api_key = get_api_key()
    if api_key:
        print(f"✅ BRAVE_SEARCH_KEY is set ({api_key[:8]}...)")
        # Try a test search
        print("   Testing API...")
        try:
            import requests
            resp = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": "test", "count": 1},
                headers={"Accept": "application/json", "X-Subscription-Token": api_key},
                timeout=5,
            )
            if resp.status_code == 200:
                print("   ✅ API is working!")
            else:
                print(f"   ⚠️  API returned {resp.status_code}")
        except Exception as e:
            print(f"   ❌ API test failed: {e}")
    else:
        print("❌ BRAVE_SEARCH_KEY not set")
        print("   Get your free key at: https://brave.com/search/api/")
        print("   The Brave Search API has a generous free tier (2000 queries/month)")


def main():
    parser = argparse.ArgumentParser(
        description="web-search: Web search and fetch CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py search "OpenClaw AI agent"
  python cli.py search "linux-server-skill" --count 10
  python cli.py fetch "https://github.com/michael-ltm/linux-server-skill"
  python cli.py summarize "https://example.com/article"
  python cli.py doctor  # Check API configuration
        """
    )
    sub = parser.add_subparsers(dest="cmd")

    # search
    s = sub.add_parser("search", help="Search the web")
    s.add_argument("query", help="Search query")
    s.add_argument("--count", "-n", type=int, default=5, help="Number of results (default: 5)")
    s.add_argument("--freshness", "-f", choices=["day", "week", "month", "year"],
                   help="Time restriction (pd/pw/pm/py)")

    # fetch
    f = sub.add_parser("fetch", help="Fetch readable content from URL")
    f.add_argument("url", help="URL to fetch")

    # summarize
    sm = sub.add_parser("summarize", help="Summarize a URL")
    sm.add_argument("url", help="URL to summarize")

    # doctor
    sub.add_parser("doctor", help="Check API configuration")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "search":
        result = do_search(args.query, count=args.count, freshness=args.freshness)
        if result is None:
            sys.exit(1)
    elif args.cmd == "fetch":
        result = do_fetch(args.url)
        if result is None:
            sys.exit(1)
    elif args.cmd == "summarize":
        do_summarize(args.url)
    elif args.cmd == "doctor":
        cmd_doctor(args)


if __name__ == "__main__":
    main()
