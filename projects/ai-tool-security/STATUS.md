# STATUS: Promising ✅

## 状态: Promising

**升级时间:** 2026-03-06

**升级理由:**
- ✅ 可运行验证通过
- ✅ 可复现用例添加
- ✅ Scanner Gate 满足 (3+ 证据)

## 检测能力 (v2)

### ✅ 已实现
- **npm/JS**: postinstall/preinstall 脚本检测
- **依赖安全**: typosquatting 检测、可疑包检测
- **GitHub Actions**: 外部 action、cache poisoning、权限检查、触发器验证
- **Prompt Injection**: Python f-string 注入检测
- **敏感文件**: .env 文件、SSH 密钥、证书检测
- **Docker**: Dockerfile 安全扫描 (root 用户、latest tag、secret)
- **Kubernetes**: K8s manifest 安全扫描
- **Terraform**: Terraform 文件 secret 检测
- **Shell**: 脚本中 hardcoded secrets 检测

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

### 用例 4: 检测 Dockerfile 安全问题
```bash
# 创建 Dockerfile
echo 'FROM node:latest
ENV API_KEY=secret
USER root' > Dockerfile

# 扫描
ai-security-scan .
# 输出: [WARNING] Container runs as root
#       [WARNING] Using 'latest' tag
#       [HIGH] Possible hardcoded secrets
```

---
*Status: Promising*
