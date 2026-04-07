#!/bin/bash
# Opportunity Research - Run after site-tracker AM/PM reports
# Usage: ./run.sh
# Output: research context written to .last_research.json

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Opportunity Research Run ($(date '+%Y-%m-%d %H:%M')) ==="

# Step 1: Select strongest signal from watchlist
echo "[1/3] Selecting strongest signal from watchlist..."
python3 research.py

if [ ! -f .last_research.json ]; then
    echo "No candidates found. Exiting."
    exit 0
fi

echo ""
echo "[2/3] Signal selected. Manual research phase:"
echo "  → Read .last_research.json for candidate details"
echo "  → Conduct web research (fetch, search)"
echo "  → Write research memo"
echo "  → Create Feishu wiki page under 机会寻找 (AS09w5D8xiq136kKJmTc7DDZnNW)"
echo "  → Append memo content + link to Feishu doc"
echo ""
echo "[3/3] See SKILL.md for full research protocol (8 questions + evidence tiers + self-check)"
echo "=== Done ==="
