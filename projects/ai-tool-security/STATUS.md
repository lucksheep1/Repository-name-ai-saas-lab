# STATUS: Promising

## 状态: Promising

**升级时间:** 2026-03-06

**升级理由:**
- ✅ 可运行验证通过
- ✅ 可复现用例添加
- ✅ Scanner Gate 满足 (3+ 证据)

## 验证步骤

```bash
# 1. 安装
pip install ai-tool-security

# 2. 扫描项目
ai-security-scan ./your-project

# 3. 严格模式
ai-security-scan ./your-project --strict
```

## 可复现用例

### 用例 1: 检测 postinstall 脚本
```bash
# 创建测试项目
mkdir test-project && cd test-project
echo '{"scripts": {"postinstall": "malicious.sh"}}' > package.json

# 扫描
ai-security-scan .
# 输出: [HIGH] postinstall script detected
```

### 用例 2: 检测 GitHub Actions 外部 action
```yaml
# .github/workflows/ci.yml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: untrusted/action@v1  # 这会被检测
```

### 用例 3: 检测 prompt injection
```python
# test.py
user_input = request.GET['prompt']
result = f"System: {user_input}"  # 这会被检测
```

---
*Status: Promising*
