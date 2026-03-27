#!/usr/bin/env python3
"""
Health Check - Check OpenClaw and system health
"""

import subprocess
import os
import json

def check_openclaw():
    """Check OpenClaw status."""
    result = subprocess.run(
        ["openclaw", "status", "--json"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            return {"status": "running", "details": data}
        except:
            return {"status": "running", "details": result.stdout[:100]}
    return {"status": "error", "details": result.stderr[:100]}

def check_crons():
    """Check cron jobs."""
    result = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True
    )
    lines = [l for l in result.stdout.split("\n") if l and not l.startswith("#")]
    return {"count": len(lines), "jobs": lines[:5]}

def check_disk():
    """Check disk usage."""
    result = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    if len(lines) > 1:
        parts = lines[1].split()
        return {"total": parts[1], "used": parts[2], "avail": parts[3], "pct": parts[4]}

def main():
    print("🏥 Health Check\n")
    
    # OpenClaw
    oc = check_openclaw()
    print(f"OpenClaw: {oc['status']}")
    
    # Cron
    crons = check_crons()
    print(f"Crons: {crons['count']} active")
    
    # Disk
    disk = check_disk()
    if disk:
        print(f"Disk: {disk['used']}/{disk['total']} ({disk['pct']})")

if __name__ == "__main__":
    main()