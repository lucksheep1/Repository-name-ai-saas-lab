#!/bin/bash
# SaaS Lab Report Cron - 定时发送报告到飞书

export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm:$PATH"
export NVM_DIR="/root/.nvm"

cd /root/.openclaw/workspace

# 读取最新报告
AM_REPORT="reports/daily_report_AM.md"
PM_REPORT="reports/daily_report_PM.md"

HOUR=$(date +%H)

if [ "$HOUR" = "09" ]; then
    REPORT_FILE="$AM_REPORT"
    REPORT_TYPE="AM"
elif [ "$HOUR" = "21" ]; then
    REPORT_FILE="$PM_REPORT"
    REPORT_TYPE="PM"
else
    exit 0
fi

if [ -f "$REPORT_FILE" ]; then
    # 读取报告内容并发送到飞书
    CONTENT=$(cat "$REPORT_FILE")
    
    # 使用 feishu API 发送消息
    # 这里通过 openclaw message 工具发送
    echo "Sending $REPORT_TYPE report..."
fi

echo "$(date): Report cron ran - Type: $REPORT_TYPE" >> /tmp/saas_lab_cron.log
