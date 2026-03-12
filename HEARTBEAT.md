# HEARTBEAT.md - Scale Gate Mode 🔒

## 阶段状态
- **模式:** Scale Gate (主项目锁定)
- **进入时间:** 2026-03-10 15:44
- **主线:** agent-memory
- **解锁时间:** 2026-03-13 15:44 (72h)

---

## Scale Gate 规则

### 1. 主线锁定
- ✅ 未来 72 小时只允许迭代 **agent-memory**
- ❌ 其他项目：只允许修 bug / 文档 / 测试，不得增加新功能与新方向

### 2. Evidence Gate 升级
- Promising/Release 只能基于"外部反馈证据"
- 禁止仅用 stars/trending 作为需求证据
- **外部反馈证据定义:** issue/PR/comment/discussion/review 的链接或编号，至少 3 条

### 3. Feedback Loop 硬目标
- **每 24 小时必须新增至少 1 条"真实反馈入口/反馈收集动作"**
- 写入 reports（例如：issue 模板、讨论区、反馈表、示例集成请求）

### 4. 报告格式升级 (AM/PM)
每次报告必须包含：
- ✅ 新增外部反馈证据（链接/编号）
- ✅ 主线项目的一个可验证里程碑（demo/集成例子/发布变更）
- ✅ 其他项目为什么暂缓（一句话）
- ✅ **Evidence delta**（新增证据清单）
- ✅ **Skill delta**（新增技能条目清单）

### 5. Evidence-First 硬门槛
- 任何机会/结论/Promising 升级 → 必须附 ≥3 条可追溯证据
- 证据优先级：A) GitHub issue/discussion/PR → B) 官方文档 → C) 技术博客
- 无外网时：用仓库内证据（skills/Research Notes + commit permalink）
- **不满足证据门槛 → 不得新增项目、不得升级 Promising**

### 6. Skill Registry 维护
- 每次遇到新问题 → 先查 skills/ 是否已有
- 无则新增 skills/<topic>/playbook.md + snippets.md
- 每轮 Scout/Scanner → 必须输出 skills/research_packs/YYYY-MM-DD.md

---

## 定时任务

### AM 汇报 (08:30-09:30)
- 检查时间：每次 heartbeat 时检查是否在 08:30-09:30 窗口
- 任务：生成 daily_report_AM.md → Git 提交 → 发送报告

### PM 汇报 (20:30-21:30)
- 检查时间：每次 heartbeat 时检查是否在 20:30-21:30 窗口
- 任务：生成 daily_report_PM.md → Git 提交 → 发送报告

---

## 执行逻辑 (Scale Gate Mode)

```
每次 heartbeat:
  获取当前时间
  
  // 汇报窗口检查
  if AM窗口:
    生成 AM 报告（含 Evidence + 里程碑 + 暂缓理由）
    Git 提交
  
  if PM窗口:
    生成 PM 报告（含 Evidence + 里程碑 + 暂缓理由）
    Git 提交
  
  // Scale Gate: 只允许主线迭代
  if 在主线锁定周期:
    只允许 agent-memory 迭代
    其他项目: bug修复/文档/测试 のみ
    每天至少1个反馈收集动作
```

---

## 状态跟踪

- **Scale Gate 状态:** 🔒 锁定中
- **主线项目:** agent-memory
- **外部反馈证据:** 5/5 ✅ (已满足)
- **当前examples:** quickstart, langchain, multi_agent, api_server
- **当前里程碑:** 迭代中 (Round 65)

---

## 备注

- 反馈收集动作记录在: analysis/scale_gate_status.md
- 外部反馈证据需 ≥3 条才能升级 STATUS
- 其他项目一律暂缓，聚焦主线突破

---
*Heartbeat: 每分钟检查一次 | Scale Gate Active*
