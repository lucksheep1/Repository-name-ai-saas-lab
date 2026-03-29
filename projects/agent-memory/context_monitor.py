#!/usr/bin/env python3
"""
Context Overflow Detector for OpenClaw agents.

Monitors context window usage and predicts when compaction will be needed,
giving agents advance warning BEFORE the 30-60 second sync compaction outage.

Background:
  OpenClaw's built-in compaction is synchronous — the agent pauses for 30-60s
  while compressing context. This is a "mini-outage" for every session.

  See: https://dev.to/oolongtea2026/external-memory-providers-zero-downtime-context-compaction-for-ai-agents-2ien

Usage:
  python context_monitor.py --session SessionName --threshold 0.75 --watch
  python context_monitor.py --session SessionName --status
  python context_monitor.py --sessions
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_THRESHOLD = 0.80  # Alert at 80% of context window
DEFAULT_WINDOW_TOKENS = 200_000  # Conservative for most LLMs
POLL_INTERVAL_SECONDS = 30
STATE_DIR = Path.home() / ".openclaw" / "memory_state"

# ---------------------------------------------------------------------------
# Token estimation (simple char-based heuristic)
# ---------------------------------------------------------------------------
CHARS_PER_TOKEN = 4  # Conservative for English+code mix


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return len(text) // CHARS_PER_TOKEN


# ---------------------------------------------------------------------------
# Session context tracking
# ---------------------------------------------------------------------------

def get_state_file(session: str) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    safe = session.replace("/", "_").replace("\\", "_")
    return STATE_DIR / f"{safe}.json"


def load_session_state(session: str) -> dict:
    path = get_state_file(session)
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "session": session,
        "messages": [],
        "total_tokens": 0,
        "last_updated": None,
        "overflow_warnings": 0,
        "last_warning_at": None,
    }


def save_session_state(session: str, state: dict) -> None:
    path = get_state_file(session)
    state["last_updated"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def add_message(session: str, role: str, content: str) -> dict:
    """Add a message to session context. Returns overflow analysis."""
    state = load_session_state(session)
    tokens = estimate_tokens(content)
    state["messages"].append({
        "role": role,
        "content_preview": content[:100],
        "tokens": tokens,
        "added_at": datetime.now().isoformat(),
    })
    state["total_tokens"] += tokens
    save_session_state(session, state)
    return analyze_overflow(state)


def analyze_overflow(state: dict) -> dict:
    """Analyze how close to context overflow."""
    total = state["total_tokens"]
    window = DEFAULT_WINDOW_TOKENS
    ratio = min(total / window, 1.0)

    # Estimate how many more messages before overflow
    avg_msg_tokens = total / max(len(state["messages"]), 1)
    remaining = window - total
    msgs_until_full = int(remaining / avg_msg_tokens) if avg_msg_tokens > 0 else 999

    return {
        "total_tokens": total,
        "context_ratio": round(ratio * 100, 1),
        "window_tokens": window,
        "messages_count": len(state["messages"]),
        "msgs_until_full": max(msgs_until_full, 0),
        "overflow_risk": (
            "CRITICAL" if ratio > 0.95
            else "HIGH" if ratio > 0.80
            else "MEDIUM" if ratio > 0.60
            else "LOW"
        ),
        "should_flush": ratio > 0.75,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_status(session: str) -> None:
    state = load_session_state(session)
    if not state["messages"]:
        print(f"Session '{session}': No messages recorded.")
        return
    analysis = analyze_overflow(state)
    print(f"\n=== Context Monitor: {session} ===")
    print(f"  Messages:      {analysis['messages_count']}")
    print(f"  Total tokens:  {analysis['total_tokens']:,} / {analysis['window_tokens']:,}")
    print(f"  Context used:  {analysis['context_ratio']}%")
    print(f"  Overflow risk: {analysis['overflow_risk']}")
    print(f"  Msgs until full: ~{analysis['msgs_until_full']}")
    print(f"  Should flush:   {'YES — trigger memory save NOW' if analysis['should_flush'] else 'No'}")
    print()


def cmd_watch(session: str, threshold: float) -> None:
    print(f"[{datetime.now():%H:%M:%S}] Watching session '{session}' "
          f"(threshold: {threshold*100:.0f}%)")
    print("Press Ctrl+C to stop.\n")

    state = load_session_state(session)
    last_warning = None

    while True:
        state = load_session_state(session)
        analysis = analyze_overflow(state)

        ratio = analysis["context_ratio"] / 100
        ts = datetime.now().strftime("%H:%M:%S")

        if ratio >= threshold:
            msg = (f"[{ts}] ⚠️  OVERFLOW WARNING: {analysis['context_ratio']}% "
                   f"({analysis['total_tokens']:,} tokens) | "
                   f"~{analysis['msgs_until_full']} msgs until compaction | "
                   f"Risk: {analysis['overflow_risk']}")
            print(msg)
            state["overflow_warnings"] += 1
            state["last_warning_at"] = datetime.now().isoformat()
            save_session_state(session, state)

            if analysis["overflow_risk"] == "CRITICAL":
                print(f"[{ts}] 🚨 CRITICAL: Compaction imminent! "
                      "Run /memory-save before context resets!")
        else:
            print(f"[{ts}] OK: {analysis['context_ratio']}% | "
                  f"{analysis['msgs_until_full']} msgs remaining | "
                  f"Risk: {analysis['overflow_risk']}")

        time.sleep(POLL_INTERVAL_SECONDS)


def cmd_sessions() -> None:
    """List all tracked sessions."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(STATE_DIR.glob("*.json"))
    if not files:
        print("No sessions tracked yet.")
        print("Usage: python context_monitor.py --add SessionName --message 'hello' 'world'")
        return
    print("\n=== Tracked Sessions ===")
    for f in files:
        try:
            with open(f) as fh:
                s = json.load(fh)
            ratio = min(s["total_tokens"] / DEFAULT_WINDOW_TOKENS, 1.0)
            updated = s.get("last_updated", "unknown")
            risk = "CRITICAL" if ratio > 0.95 else "HIGH" if ratio > 0.80 else "MEDIUM" if ratio > 0.60 else "LOW"
            print(f"  {s['session']:<30} {ratio*100:5.1f}%  {risk:<8}  {len(s['messages']):>3} msgs  updated: {updated}")
        except (json.JSONDecodeError, KeyError):
            print(f"  {f.stem}  (corrupted)")
    print()


def cmd_add_message(session: str, content: list) -> None:
    """Add one or more messages to a session."""
    combined = " ".join(content)
    result = add_message(session, role="user", content=combined)
    print(f"Added message ({estimate_tokens(combined):,} tokens) to '{session}'")
    print(f"  Context: {result['context_ratio']}% | Risk: {result['overflow_risk']}")
    if result["should_flush"]:
        print(f"  ⚠️  Recommendation: Flush memory before overflow!")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Context Overflow Detector — predict and prevent OpenClaw compaction outages",
        epilog="External Memory Provider concept: https://dev.to/oolongtea2026/external-memory-providers-zero-downtime-context-compaction-for-ai-agents-2ien"
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("sessions", help="List all tracked sessions")

    p_status = sub.add_parser("status", help="Show context status for a session")
    p_status.add_argument("--session", required=True, help="Session name")

    p_watch = sub.add_parser("watch", help="Monitor a session continuously")
    p_watch.add_argument("--session", required=True, help="Session name")
    p_watch.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                         help=f"Alert threshold 0.0–1.0 (default: {DEFAULT_THRESHOLD})")

    p_add = sub.add_parser("add", help="Add a message and analyze overflow")
    p_add.add_argument("--session", required=True, help="Session name")
    p_add.add_argument("content", nargs="+", help="Message content (will be joined)")

    p_reset = sub.add_parser("reset", help="Reset/clear a session")
    p_reset.add_argument("--session", required=True, help="Session name")

    args = parser.parse_args()

    if args.cmd == "sessions":
        cmd_sessions()
    elif args.cmd == "status":
        cmd_status(args.session)
    elif args.cmd == "watch":
        cmd_watch(args.session, args.threshold)
    elif args.cmd == "add":
        cmd_add_message(args.session, args.content)
    elif args.cmd == "reset":
        path = get_state_file(args.session)
        if path.exists():
            path.unlink()
        print(f"Session '{args.session}' reset.")
    else:
        parser.print_help()
