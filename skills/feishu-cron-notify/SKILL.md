---
name: feishu-cron-notify
description: Feishu notification skill for cron or scheduled task completion. Sends result notifications after a task finishes.
---

# feishu-cron-notify

## purpose

Send a Feishu notification after a cron or scheduled task finishes.
This skill is only about post-task notification, not task execution.

## when_to_use

- When a cron or scheduled job needs a completion notification
- When the operator wants success or failure to be delivered to Feishu after a run

## do_not_use_for

- Running the primary task itself
- Replacing archival workflows
- General chat delivery unrelated to task completion

## inputs

- task_name
- execution_result: success or failure
- completion_time
- summary_message
- optional target user or target chat override

## outputs

- notification status
- target destination
- delivery method used
- failure reason if notification was not sent

## required_dependencies

- one of: `feishu_chat` tool, OpenClaw local agent invocation, or `FEISHU_WEBHOOK_URL`
- optional routing vars: `FEISHU_TARGET_USER`, `FEISHU_TARGET_CHAT`

## current_status

- formal retained version: yes
- duplicate copy in `/root/.openclaw/skills/`: disabled in batch 1
- dependency readiness: unverified in this batch
- webhook / chat target configuration: unverified in this batch

## fallback

- If no Feishu delivery path is configured: report notification unavailable
- If the main task succeeded but notification failed: report task result and notification failure separately
- No fallback delivery channel is defined by this skill

## input_prerequisites

Before using this skill, the caller should know:
- which task just finished
- whether it succeeded or failed
- what message should be delivered
- which target should receive the notification, if default routing is not desired

## minimum_output_template

```text
status: success | failure
target_destination: <user/chat/webhook or unresolved>
delivery_method: feishu_chat | openclaw_agent | webhook | unavailable
failure_reason: <none or concrete reason>
```

## 配置

### 环境变量

- `FEISHU_WEBHOOK_URL`: 飞书 Webhook URL（可选，用 message tool 时不需要）
- `FEISHU_TARGET_USER`: 目标用户 open_id（默认: ou_a5226fe51a08a61cd82f0fcf10da7be8）
- `FEISHU_TARGET_CHAT`: 目标群组 chat_id（可选）

### 在 Cron 中使用

#### 方案 1: 使用 OpenClaw Agent (推荐)

```bash
0 9 * * * /root/.local/share/pnpm/openclaw agent --local --agent main --timeout 600 --message '运行 site-tracker，然后使用 feishu_chat 工具发送报告给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8' >> /tmp/cron.log 2>&1
```

#### 方案 2: 脚本中调用

在定时脚本末尾添加飞书通知调用。

#### 方案 3: 使用 message tool (需要 OpenClaw 环境)

```bash
cd /root/.openclaw/workspace
/root/.local/share/pnpm/openclaw agent --local --agent main --timeout 60 --message "使用 feishu_chat 工具发送消息 '任务完成' 给 user:ou_a5226fe51a08a61cd82f0fcf10da7be8"
```

## 最佳实践

1. 始终在 cron 任务后添加通知
2. 通知包含时间、任务名、结果、错误
3. 失败时也发送告警
4. 使用 OpenClaw Agent 优于直接 Webhook
