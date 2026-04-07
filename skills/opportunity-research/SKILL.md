---
name: opportunity-research
description: |
  Signal-driven opportunity research skill. Runs after site-tracker AM/PM reports.
  Activated automatically by heartbeat, or manually after "飞书存档" workflow.
  Selects strongest signal from watchlist, outputs formal research memo to Feishu wiki (机会寻找 folder).
---

# 机会研究 skill

## 定位

**一句话：** 从 site-tracker 的 watchlist 中自主选择最强信号，对单个项目做正式研究，输出 research memo 到飞书。

**边界：** 不负责抓取，不负责立项设计。负责把信号变成研究结论。

---

## 自动触发

每天 AM 报告（08:30-09:30）和 PM 报告（20:30-21:30）之后各运行一次。

---

## 运行步骤

### Step 1 — 信号选择（research.py）

```bash
cd /root/.openclaw/workspace/projects/opportunity-research
./run.sh
```

`research.py` 从 `projects/site-tracker/tracker.db` 的 watchlist 中按以下优先级选最强信号：

1. **多源共振优先** — 同一项目被 ≥2 个独立来源标记
2. **单源持续次之** — 单来源 + 高重复出现次数

输出到 `.last_research.json`。

### Step 2 — 研究执行

读取 `.last_research.json`，获取候选项目信息，然后：
1. Fetch 项目主页 / GitHub / 官网
2. 找竞品 / 替代品
3. 对比分析
4. 赛道归纳
5. 回答8个必答问题 + 给出后续验证信号

### Step 3 — 飞书存档

创建飞书 wiki 页面（parent: `AS09w5D8xiq136kKJmTc7DDZnNW`，space: `7522776428406849538`），写入完整 memo。

---

## 研究报告格式规范（v1.2+）

### 标题区（必须包含）

```
signal类型: signal:single_source_persistent | signal:multi_source_resonance
证据最高等级: L1 / L2 / L3 / L4
保守程度: 偏保守 / 中性 / 偏积极
```

### 正文区（必须包含）

- 所有数字带 `[📦L1]` / `[📝L2]` / `[📰L3]` / `[🔮L4]` 标注
- 无裸数字
- 外部对标数字：竞品用户/收入/融资额 查不到 L3+ 出处 → 必须改写为定性表述
- 创业切入建议：只到 工具 / SaaS / 内容 / 服务 / 数据 形态层，不落地具体行业

### 页脚区（必须包含）

```
首轮自检: ✅通过 / ❌不通过
signal类型: (与标题区一致)
证据最高等级: (与标题区一致)
保守程度: (与标题区一致)
```

### 8个必答问题

1. 为什么研究它（signal来源 + 选中理由）
2. 它是什么（项目本身 + 给谁用 + 解决什么）
3. 它为什么现在出现（技术/成本/需求/分发变化）
4. 它和谁像、和谁不同（竞品对比 + 差异化）
5. 它背后是什么赛道（上升到赛道层理解）
6. 这个赛道有没有创业选题价值（判断 + 理由）
7. 更适合什么切入方式（工具/SaaS/内容/服务/数据）
8. 最后的判断（积极/中性/谨慎 + 是否值得继续跟踪）

### 首轮自检清单

```
1. signal类型已明确标注
2. 所有数字已分级标注（L1-L4），无裸数字
3. 创业切入建议只到形态层，无具体行业落地
4. 8个必答问题全部覆盖，无跳答
5. 后续验证信号已给出（判断正确信号 + 降优先级信号）
6. 标题区 / 正文区 / 页脚区 三区证据等级一致
7. 外部对标数字有据可查（用户/收入/融资额无L4裸写）
8. 结论保守程度与signal类型匹配
```

---

## 飞书目录

- **Space ID:** `7522776428406849538`
- **机会寻找 node:** `AS09w5D8xiq136kKJmTc7DDZnNW`

---

## 文件结构

```
projects/opportunity-research/
├── research.py      # 信号选择脚本（读取watchlist，输出.json）
├── run.sh           # 调度入口（被heartbeat调用）
├── .last_research.json  # 最近一次研究输入（临时文件，gitignore）
└── tracking.md      # 跟踪事项（进行中 + 已关闭）

skills/opportunity-research/
└── SKILL.md         # 本文件
```

## 跟踪事项写入规范

研究报告完成后，将「后续验证信号」同步追加到 `projects/opportunity-research/tracking.md`：

```markdown
### YYYY-MM-DD | 项目名
**signal:** ... | **报告位置:** [wiki链接]

**→ 判断正确应看到的信号：**
- [ ] 信号1
- [ ] 信号2

**→ 降低优先级应出现的信号：**
- [ ] 信号A

**下次检查日期:** YYYY-MM-DD（+7天）
```

每次 AM/PM heartbeat 检查 tracking.md，如有信号出现 → 勾选并移至已关闭。
