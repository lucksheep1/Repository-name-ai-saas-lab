# HEARTBEAT.md

# AI SaaS Lab - 定时汇报配置

## 定时任务

### AM 汇报 (08:30-09:30)
- 检查时间：每次 heartbeat 时检查是否在 08:30-09:30 窗口
- 任务：生成 daily_report_AM.md 并提交 Git

### PM 汇报 (20:30-21:30)
- 检查时间：每次 heartbeat 时检查是否在 20:30-21:30 窗口
- 任务：生成 daily_report_PM.md 并提交 Git

### 无限循环 (每次 heartbeat)
- 执行 Scout → Scanner → Builder → Analyst → Evolution
- 每轮结束 Git 提交

## 执行逻辑

```
每次 heartbeat (每分钟):
  获取当前时间 (hour, minute)
  
  // 汇报窗口检查
  if (hour == 8 and minute >= 30) or (hour == 9 and minute <= 30):
    if 今天还未生成 AM 报告:
      生成 AM 报告
      Git 提交并推送
      标记 AM 已完成
  
  if (hour == 20 and minute >= 30) or (hour == 21 and minute <= 30):
    if 今天还未生成 PM 报告:
      生成 PM 报告
      Git 提交并推送
      标记 PM 已完成
  
  // 无限循环 - 每轮 Scout 开始
  执行 Scout 阶段
  如果发现机会，进入 Scanner → Builder → Analyst → Evolution
  Git 提交
```

## 状态跟踪

- last_AM_report: 2026-03-06 10:11
- last_PM_report: 2026-03-06 20:33
- current_round: 18

---
*Heartbeat: 每分钟检查一次*
