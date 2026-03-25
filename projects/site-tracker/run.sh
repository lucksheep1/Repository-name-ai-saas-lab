#!/bin/bash
# Site Tracker 调度脚本 - 每12小时运行一次
# 
# 使用方法:
#   手动运行: ./run.sh
#   添加到 crontab: crontab -e
#   添加行: 0 */12 * * * /path/to/run.sh >> /path/to/tracker.log 2>&1
#
# 报告输出: reports/report_YYYYMMDD_HHMM.md

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 创建报告目录
mkdir -p reports

# 生成报告文件名
TIMESTAMP=$(date +%Y%m%d_%H%M)
REPORT_FILE="reports/report_${TIMESTAMP}.md"

echo "=== Site Tracker 运行中 (${TIMESTAMP}) ==="

# 运行 tracker
python3 tracker.py run 2>&1 | tee /tmp/tracker_run.log

# 生成报告 (捕获输出)
python3 - "$REPORT_FILE" "$TIMESTAMP" <<'PYEOF'
import sqlite3
from datetime import datetime

DB = "tracker.db"
REPORT_FILE = __import__('sys').argv[1]
TIMESTAMP = __import__('sys').argv[2]

conn = sqlite3.connect(DB)
now = datetime.now().strftime("%Y-%m-%d %H:%M")

# 获取统计
total = conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]

# 本次运行统计
last_run = conn.execute("""
    SELECT MAX(started_at) FROM runs WHERE completed_at IS NOT NULL
""").fetchone()[0]

new_this_run = 0
updated_this_run = 0
if last_run:
    new_this_run = conn.execute("""
        SELECT COUNT(*) FROM opportunities WHERE first_seen_at > ?
    """, (last_run,)).fetchone()[0]
    
    updated_this_run = conn.execute("""
        SELECT COALESCE(SUM(appearance_count - 1), 0) FROM opportunities WHERE last_seen_at > ? AND first_seen_at <= ?
    """, (last_run, last_run)).fetchone()[0]

# Source quality
quality = conn.execute("""
    SELECT source, success_count, noisy_count, last_success_at 
    FROM source_quality ORDER BY success_count DESC
""").fetchall()

# Watchlist - 取唯一的
watchlist = conn.execute("""
    SELECT w.source, o.title, w.reason, o.appearance_count, o.last_seen_at
    FROM watchlist w 
    JOIN opportunities o ON w.opportunity_id = o.id
    GROUP BY o.title
    ORDER BY o.appearance_count DESC, w.flagged_at DESC
    LIMIT 20
""").fetchall()

# 生成报告
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# Site Tracker 报告\n\n")
    f.write(f"**生成时间**: {now}\n\n")
    f.write(f"## 运行统计\n\n")
    f.write(f"| 指标 | 数值 |\n")
    f.write(f"|------|------|\n")
    f.write(f"| 总机会数 | {total} |\n")
    f.write(f"| 本次新增 | {new_this_run} |\n")
    f.write(f"| 本次更新 | {updated_this_run} |\n\n")
    
    f.write(f"## 来源质量\n\n")
    f.write(f"| 来源 | 成功 | 噪音 | 最后成功 |\n")
    f.write(f"|------|------|------|----------|\n")
    for q in quality:
        last = q[3][:19] if q[3] else "无"
        f.write(f"| {q[0]} | {q[1]} | {q[2]} | {last} |\n")
    
    f.write(f"\n## 观察清单 (Watchlist)\n\n")
    f.write(f"| 来源 | 标题 | 标记原因 | 出现次数 |\n")
    f.write(f"|------|------|----------|----------|\n")
    for w in watchlist:
        title = w[1][:30] + "..." if len(w[1]) > 30 else w[1]
        f.write(f"| {w[0]} | {title} | {w[2]} | {w[3]} |\n")
    
    f.write(f"\n## 说明\n\n")
    f.write(f"- **标记规则**: high_signal_source=高价值来源(GitHub/OpenAlternative), keyword=关键词匹配(ai/agent/llm等)\n")
    f.write(f"- **调度设置**: 每12小时运行，cron 表达式 `0 */12 * * *`\n")
    f.write(f"- **报告位置**: {REPORT_FILE}\n")
    f.write(f"- **查看watchlist**: `python tracker.py watchlist`\n")
    f.write(f"- **查看来源质量**: `python tracker.py quality`\n")

conn.close()
print(f"\n报告已生成: {REPORT_FILE}")
PYEOF

echo ""
echo "=== 完成 ==="
echo "报告: $REPORT_FILE"