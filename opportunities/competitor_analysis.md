# Competitor Analysis — 2026-03-06

## Opportunity: AI Tool Security Scanner

### Existing Solutions

1. **trivy**
   - 定位: 传统安全扫描
   - 优点: 功能全面，成熟
   - 问题: 不检测 prompt injection，不针对 AI 工具

2. **snyk**
   - 定位: 企业安全
   - 优点: 全面
   - 问题: 昂贵，不针对 AI 特有攻击

3. **GitHub Advanced Security**
   - 定位: GitHub 原生安全
   - 优点: 深度集成
   - 问题: 付费，不检测 AI prompt injection

### Competitor Problems

- 缺乏针对 AI 工具的安全检测
- 缺乏 prompt injection 检测
- 缺乏轻量级开源方案

### Improvement Opportunity

做一个轻量级 AI 工具安全扫描器：
- GitHub Actions workflow 安全检测
- npm package.json postinstall 检测
- prompt injection 模式检测

### Differentiation

- **专注 AI**: 针对 AI 工具特有攻击
- **轻量**: CLI 工具，快速安装
- **开源**: 免费，社区驱动
- **简单**: 不需要复杂配置

---
*Competitor Analysis: 2026-03-06 10:25 GMT+8*
