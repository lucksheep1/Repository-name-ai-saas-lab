#!/usr/bin/env python3
"""
Cron Check - Verify OpenClaw cron jobs
"""

import json
import os

CRON_FILE = "/root/.openclaw/cron/jobs.json"

def check_crons():
    """Check cron jobs status."""
    if not os.path.exists(CRON_FILE):
        print("❌ No cron jobs file found")
        return
    
    with open(CRON_FILE, "r") as f:
        data = json.load(f)
    
    jobs = data.get("jobs", [])
    
    if not jobs:
        print("📭 No cron jobs configured")
        print("   To add: edit /root/.openclaw/cron/jobs.json")
        return
    
    print(f"⏰ {len(jobs)} cron jobs:\n")
    for job in jobs:
        print(f"  - {job.get('name', 'unnamed')}")
        print(f"    Schedule: {job.get('schedule', 'N/A')}")
        print(f"    Command: {job.get('command', 'N/A')[:50]}...")
        print()

if __name__ == "__main__":
    check_crons()