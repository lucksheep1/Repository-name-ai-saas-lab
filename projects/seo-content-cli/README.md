# SEO Content CLI

命令行 SEO 内容生成工具。

## Problem

seomachine 证明 SEO 内容生成是真实需求，但缺乏开源 CLI 替代品。

## Solution

纯 CLI 开源工具，快速生成 SEO 优化内容：
- 单篇生成
- 批量处理
- 自定义模板

## Usage

```bash
# 单篇生成
python3 seo_content.py --keyword "Python Tutorial" --title "Learn Python Fast"

# 输出到文件
python3 seo_content.py -k "AI Tools" -t "Best AI Tools 2024" -o article.md

# 批量生成 (每行一个关键词)
python3 seo_content.py --keywords keywords.txt --batch

# 自定义 API (需要 Claude API key)
python3 seo_content.py -k "SEO" --api-key sk-xxx
```

## Verification

```bash
# 测试运行
python3 seo_content.py --keyword "Test Keyword" --title "Test Title"
```

## Limits

- 当前版本使用模板生成，非真正的 LLM 调用
- 需配置 API key 才能使用完整功能

## Next

- [ ] 接入 Claude API
- [ ] 添加更多模板
- [ ] 支持自定义 prompt

---
*Created: 2026-03-05*
*Status: Experiment*
