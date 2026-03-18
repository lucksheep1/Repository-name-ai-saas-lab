#!/bin/bash
# Feedback Collector - 自动收集反馈脚本

# 使用方法:
# ./scripts/feedback_collector.sh --collect --feature "web_dashboard" --price "5" --email "test@example.com"

COLLECT_ENDPOINT="https://httpbin.org/post"

collect_feedback() {
    local feature="$1"
    local price="$2"
    local email="$3"
    
    echo "Collecting feedback..."
    curl -s -X POST "$COLLECT_ENDPOINT" \
        -d "feature=$feature&price=$price&email=$email" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('Feedback submitted!')
print(f'Feature: {d.get(\"form\", {}).get(\"feature\")}')
print(f'Price: {d.get(\"form\", {}).get(\"price\")}')
"
}

# 解析参数
if [ "$1" = "--collect" ]; then
    collect_feedback "$2" "$4" "$6"
fi
