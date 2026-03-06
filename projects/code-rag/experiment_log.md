# Experiment Log

## 2026-03-06 - MVP Build

### Approach
使用 TF-IDF 构建本地代码搜索：
- 提取代码块
- 构建 TF-IDF 索引
- 余弦相似度搜索

### Result
~180 行核心代码，支持多种语言

### Next Steps
- [ ] 测试真实代码库
- [ ] 添加语义嵌入
- [ ] 添加更多语言
