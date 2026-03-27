# HEARTBEAT.md - Founder Mode

## 阶段状态
- **模式:** Founder Mode (Agent-Native Startup) ⚡
- **激活时间:** 2026-03-17 22:58
- **主线:** agent-memory
- **状态:** 🔓 已解锁

---

## Founder Mode 核心要求

### 每日硬要求
每24小时必须产出至少一个"对外可见"的东西：
- ✅ 一个真实可运行 demo
- ✅ 一个可发布的小工具
- ✅ 一个更锋利的 landing / README
- ✅ 一个新的 agent-native 示例
- ✅ 一个 release note
- ✅ 一个明确的 feedback hook

### 今日产出 (2026-03-28)
- [x] AM 汇报 (08:06) ✅ - 发送至飞书
- [x] Cycle 39 - 新域 scout (AI Agent DevOps Skills / linux-server-skill) ✅
- [x] Cycle 40 - dashboard.py (HTML Analytics) ✅
- [x] Cycle 41 - git-memory (Natural Language Git History Q&A) ✅
- [x] Cycle 42 - skill-builder (OpenClaw SKILL.md Generator) ✅
- [x] Cycle 43 - web-search (Brave Search + URL Fetch CLI) ✅
- [ ] AM 汇报 (03-28 08:30-09:30)
- [ ] PM 汇报 (03-28 20:30-21:30)

---

## 定时任务

### AM 汇报 (08:30-09:30)
- 检查时间：每次 heartbeat 时检查是否在 08:30-09:30 窗口
- 任务：生成 Founder Update 风格报告

### PM 汇报 (20:30-21:30)
- 检查时间：每次 heartbeat 时检查是否在 20:30-21:30 窗口
- 任务：生成 Founder Update 风格报告

### Site Tracker 报告 (09:00 & 20:00)
- 检查时间：每天 08:55-09:05 和 19:55-20:05
- 任务：运行 site-tracker 并发送报告至飞书
- 命令：`cd projects/site-tracker && ./run.sh`

---

## 执行逻辑

```
每次 heartbeat:
  获取当前时间
  
  // 汇报窗口检查
  if AM窗口 (08:30-09:30):
    生成 Founder Update 报告 (5个问题)
    发送至飞书 (message tool)
    Git 提交
  
  if Site Tracker AM窗口 (08:55-09:05):
    运行 site-tracker (cd projects/site-tracker && ./run.sh)
    发送报告至飞书
  
  if PM窗口 (20:30-21:30):
    生成 Founder Update 报告 (5个问题)
    发送至飞书 (message tool)
    Git 提交

  if Site Tracker PM窗口 (19:55-20:05):
    运行 site-tracker
    发送报告至飞书
  
  // Founder Mode 迭代
  执行: 押注 → 实验 → 获取反馈 → 判断 → 迭代/切换
```

---

## Founder Update 报告格式

每次 AM/PM 只回答 5 个问题：
1. 我今天押注了什么？
2. 我今天砍掉了什么？
3. 我今天做了哪个最小实验？
4. 我今天从外部世界学到了什么？
5. 我明天会继续加码还是切换？

---

## 状态跟踪

- **Founder Mode:** ⚡ 已激活 (2026-03-17 22:58)
- **主线项目:** agent-memory v3.1 (Promising 48/50)
- **24h 目标:** GitHub Pages 访问信号 📊
- **押注方向:** Agent Memory v3.1 (TTL + Encryption + Redis)
- **砍掉方向:** Python 示例生态 (已超 1600，转向功能开发)

---

## 备注

- 已进入 Founder Mode
- 速度优先于完整
- 对外可见优先于内部准备
- ⚠️ 不再新增 Python 示例（>1600 已足够）
- v3.1: String TTL ✅, Encryption ✅, Redis 后端 🔧

---
*Heartbeat: 每分钟检查一次 | Founder Mode Activated*
