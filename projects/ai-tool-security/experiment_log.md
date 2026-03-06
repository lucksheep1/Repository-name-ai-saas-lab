# Experiment Log

## 2026-03-06 - MVP Build

### Attempt 1: Full security suite
**Idea:** Complete security platform with ML-based detection
**Problem:** Too complex, 4+ 小时无法完成
**Solution:** Pivot to rule-based CLI scanner

### Attempt 2: Only GitHub Actions
**Idea:** Focus only on GitHub Actions security
**Problem:** 范围太窄
**Solution:** Add npm package.json and Python support

### Final: Multi-target scanner
**Approach:**
- GitHub Actions workflow 扫描
- npm package.json 扫描
- Python prompt injection 检测

**Result:** ~200 行核心代码，支持多种目标

### Next Steps
- [ ] Test with real repositories
- [ ] Add GitHub API integration
- [ ] Add more detection patterns
