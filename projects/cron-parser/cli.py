#!/usr/bin/env python3
"""
Cron Expression Parser - Parse and validate cron expressions
"""

import argparse
from datetime import datetime

# Simple cron parser
CRON_HELP = """
Cron format: minute hour day month weekday

Examples:
  * * * * *     - Every minute
  0 9 * * *    - Every day at 9:00
  0 8 * * 1-5  - Weekdays at 8:00
  */5 * * * *  - Every 5 minutes
"""

def parse_cron(expr):
    """Parse cron expression."""
    parts = expr.split()
    if len(parts) != 5:
        return None
    return {"minute": parts[0], "hour": parts[1], "day": parts[2], "month": parts[3], "weekday": parts[4]}

def next_run(expr):
    """Calculate next run time (simplified)."""
    parsed = parse_cron(expr)
    if not parsed:
        return "Invalid expression"
    return "Use crontab.guru to calculate"

def main():
    parser = argparse.ArgumentParser(description="Cron Expression Parser")
    parser.add_argument("expr", nargs="?", help="Cron expression")
    parser.add_argument("--next", action="store_true", help="Show next run time")
    parser.add_argument("--help-cron", action="store_true", help="Show cron format help")
    
    args = parser.parse_args()
    
    if args.help_cron:
        print(CRON_HELP)
        return
    
    if not args.expr:
        print(CRON_HELP)
        return
    
    parsed = parse_cron(args.expr)
    if parsed:
        print(f"✅ Valid: {args.expr}")
        if args.next:
            print(f"Next: {next_run(args.expr)}")
    else:
        print(f"❌ Invalid: {args.expr}")

if __name__ == "__main__":
    main()