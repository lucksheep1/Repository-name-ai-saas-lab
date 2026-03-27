#!/bin/bash
# Feishu Cron Notify Script
# 用法: ./notify.sh "消息内容" [target_user_open_id]

TARGET_USER="${2:-ou_a5226fe51a08a61cd82f0fcf10da7be8}"

cd /root/.openclaw/workspace

# 使用 OpenClaw Agent 发送飞书消息
/root/.local/share/pnpm/openclaw agent --local --agent main --timeout 60 --message "使用 feishu_chat 工具发送消息 '$1' 给 user:$TARGET_USER" >> /tmp/feishu_notify.log 2>&1

echo "通知已发送: $1"