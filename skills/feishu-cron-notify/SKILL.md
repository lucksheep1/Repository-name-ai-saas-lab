# feishu-cron-notify

Feishu 定时任务通知 Skill。确保每个 cron 任务完成后自动发送通知。

## 功能

- 定时任务完成后自动发送飞书通知
- 支持自定义消息模板
- 支持目标用户/群组配置

## 配置

### 环境变量

- `FEISHU_WEBHOOK_URL`: 飞书 Webhook URL（可选，用 message tool 时不需要）
- `FEISHU_TARGET_USER`: 目标用户 open_id（默认: ou_a5226fe51a08a61cd82f0fcf10da7be8）
- `FEISHU_TARGET_CHAT`: 目标群组 chat_id（可选）

### 在 Cron 中使用

#### 方案 1: 使用 OpenClaw Agent (推荐)

```bash
# 在 crontab 中配置 OpenClaw agent 调用
0 9 * * * /root/.local/share/pnpm/openclaw agent --local --agent main --timeout 600 --message '运行 site-tracker，然后使用 feishu_chat 工具发送报告给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8' >> /tmp/cron.log 2>&1
```

#### 方案 2: 脚本中调用

在定时脚本末尾添加飞书通知调用：

```python
# Python 脚本
import subprocess

# ... 你的任务逻辑 ...

# 发送飞书通知
result = subprocess.run([
    "python3", "-c", """
from urllib.request import Request, urlopen
import json

msg = {
    "msg_type": "text",
    "content": {"text": "✅ 任务完成\\n时间: 2026-03-27 09:55\\n结果: 成功"}
}

req = Request(
    "YOUR_WEBHOOK_URL",
    data=json.dumps(msg).encode(),
    headers={"Content-Type": "application/json"}
)
urlopen(req)
"""
])
```

#### 方案 3: 使用 message tool (需要 OpenClaw 环境)

```bash
# 创建 notify.sh 脚本
#!/bin/bash
cd /root/.openclaw/workspace
/root/.local/share/pnpm/openclaw agent --local --agent main --timeout 60 --message "使用 feishu_chat 工具发送消息 '任务完成' 给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8"
```

## 最佳实践

1. **始终在 cron 任务后添加通知** - 不允许任何静默完成的定时任务
2. **通知包含关键信息** - 时间、任务名、结果、错误（如有）
3. **失败时也要通知** - 任务失败时发送告警消息
4. **使用 OpenClaw Agent** - 优于直接调用 Webhook，更可靠

## 示例 Cron 配置

```bash
# Site Tracker 早报 (每天 08:55)
55 8 * * * cd /root/.openclaw/workspace/projects/site-tracker && ./run.sh >> /tmp/site_tracker.log 2>&1 && /root/.local/share/pnpm/openclaw agent --local --agent main --timeout 120 --message '读取 projects/site-tracker/reports/report_*.md 文件内容，使用 feishu_chat 工具发送给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8' >> /tmp/notify.log 2>&1

# Site Tracker 晚报 (每天 20:55)
55 20 * * * cd /root/.openclaw/workspace/projects/site-tracker && ./run.sh >> /tmp/site_tracker.log 2>&1 && /root/.local/share/pnpm/openclaw agent --local --agent main --timeout 120 --message '读取 projects/site-tracker/reports/report_*.md 文件内容，使用 feishu_chat 工具发送给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8' >> /tmp/notify.log 2>&1
```

## 验证

- [ ] Cron 任务执行
- [ ] 任务完成后通知发送
- [ ] 通知包含任务结果
- [ ] 失败时发送告警