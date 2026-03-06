# Experiment Log

## 2026-03-06 - v2.0 迭代

### 新增功能

1. **typosquatting 检测**
   - 检测 npm, pip, git 的仿冒包名
   - 基于已知攻击模式

2. **Prompt Injection 模式扩展**
   - 新增 4 种检测模式
   - 覆盖常见攻击向量

3. **多语言支持**
   - 添加 JS/TS 扫描
   - process.env 秘密检测

4. **严格模式**
   - 添加 --strict 选项
   - 更严格的检测规则

### Result
代码从 ~200 行扩展到 ~300 行
功能增加 50%+

### Next Steps
- [ ] 测试真实项目
- [ ] 添加 GitHub API 集成
